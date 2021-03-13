import requests
import json
import base64
from pprint import pprint
from github import Github
from collections import deque
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings as django_settings
from django.core import serializers
from django.views import View
from django.views.generic import DetailView, ListView, CreateView
from django.views.generic.edit import FormMixin
from django.utils import timezone

from .models import (
    GithubUser, 
    GithubRepo, 
    RepoCommit, 
    RepoContentFile, 
    FileComment
)

G_TOKEN = django_settings.GITHUB_TOKEN
G_USERNAME = django_settings.GITHUB_USERNAME
github = Github(G_TOKEN)

class SearchGithub(View):    
    def post(self, request, *args, **kwargs):
        """
        all the related methods below return a qs or None for consistency
        """
        # init
        self.max_num_items = 5
        
        # POST request
        search_word = request.POST.get('search_word')
        print('## searching for: ', search_word)
        
        # check if user in db -> return None if not found
        exact_user, github_users = self.get_github_users(search_word)
        
        # check if repo in db -> return None if not found
        exact_repo, github_repos = self.get_github_repos(search_word)
        
        # no exact user in db -> check with github API
        if (not exact_user) and ("/" not in search_word):
            exact_user = self.update_or_create_github_user(search_word)
        
        # no exact repo in db and there is possible repo name -> check with github API
        if (not exact_repo) and ("/" in search_word) and (search_word.find("/") + 1 < len(search_word)):
            exact_repo = self.update_or_create_github_repo(search_word)
        
        # serialize qs
        exact_user = self.serializeQs(exact_user)
        exact_repo = self.serializeQs(exact_repo)
        github_users = self.serializeQs(github_users)
        github_repos = self.serializeQs(github_repos)
        context = {
            'exact_user': exact_user,
            'exact_repo': exact_repo,
            'github_users': github_users,
            'github_repos': github_repos,
        }
        return HttpResponse(json.dumps(context), content_type='application/json')
    
    def get_github_users(self, search_word):
        # check for exact user in db
        exact_user = GithubUser.objects.filter(username__iexact=search_word) or None

        # seach for close matches and exclude exact match
        github_users = GithubUser.objects.filter(
            username__contains=search_word
        ).exclude(
            username__iexact=search_word
        )[:self.max_num_items] or None
        
        print('## exact_user in db:', exact_user)
        return exact_user, github_users

    def get_github_repos(self, search_word):
        # check for exact repo in db, consider path lookup also
        exact_repo = GithubRepo.objects.filter(name__iexact=search_word) or None
        if "/" in search_word:
            exact_repo = GithubRepo.objects.filter(path__iexact=search_word) or None

        # seach for close matches and exclude exact match
        github_repos = GithubRepo.objects.filter(
            name__contains=search_word
        ).exclude(
            name__iexact=search_word
        )[:self.max_num_items] or None
        if "/" in search_word:
            github_repos = GithubRepo.objects.filter(
                path__contains=search_word
            ).exclude(
                path__iexact=search_word
            )[:self.max_num_items] or None
        print('## exact_repo in db:', exact_repo)
        return exact_repo, github_repos
        
    def update_or_create_github_user(self, search_word):
        # use github API to see if username exists and create Github User
        try: 
            new_user = github.get_user(search_word)
            _, created = GithubUser.objects.update_or_create(
                username=new_user.login,
            )
            exact_user = GithubUser.objects.filter(username=new_user.login) # to get a qs
            print('## Github user:', search_word)
            print('## created:', created)
        except: 
            exact_user = None
        print("## github search user result:", exact_user)
        return exact_user 

    def update_or_create_github_repo(self, search_word):
        # check username in db and create if !exists
        username = search_word[:search_word.find("/")]
        exact_user = self.update_or_create_github_user(username)[0]
        print('## create_github_repo -> exact_user:', exact_user)
        
        # time is UTC based
        if exact_user:
            # use github API to see if repo exists and create Github Repo
            try:
                repo = github.get_repo(search_word)
                _, created = GithubRepo.objects.update_or_create(
                    name=repo.name,
                    owner=exact_user,
                    created_at=repo.created_at + timedelta(hours=9),
                    path=repo.full_name,          
                    defaults={
                        'description': repo.description,
                        'pushed_at': repo.pushed_at + timedelta(hours=9),
                        'homepage': repo.homepage,
                        'number_of_commits': repo.get_commits().totalCount,  
                    }
                )
                print('## repo from github created:', created)
                exact_repo = GithubRepo.objects.filter(
                    name=repo.name,
                    owner=exact_user,
                    path=repo.full_name,
                )
            except:
                exact_repo = None
        else:
            exact_repo = None
        print('## new repo added to db:', exact_repo)
        return exact_repo
    
    def serializeQs(self, qs):
        if qs:
            return serializers.serialize('json', qs)
        return None
    
class UserDetailView(View):    
    def get(self, request, *args, **kwargs):
        # get requested user data
        user_pk = kwargs.get('pk')
        requested_user = GithubUser.objects.get(pk=user_pk)
        
        # get related repos from db
        requested_repos = GithubRepo.objects.filter(owner=requested_user).order_by('-pushed_at')

        # if no repos in db
        if not requested_repos:
            repos = self.get_repos_from_API(requested_user.username)
            requested_repos = self.update_or_create_github_repos(requested_user, repos)
        else:
            print('## repo data from db')
        context = {
            'requested_user': requested_user,
            'requested_repos': requested_repos,
        }
        return render(request, 'gitAPI/user_detail.html', context)
    
    def post(self, request, *args, **kwargs):
        # get GithubUser
        requested_username = request.POST.get('username')
        requested_user = GithubUser.objects.get(username=requested_username)
        print('## last_repos_update updated for', requested_username, 'to', timezone.now())
        
        # update GithubRepos
        repos = self.get_repos_from_API(requested_user.username)
        requested_repos = self.update_or_create_github_repos(requested_user, repos)
        print('## repos in db updated')
        return HttpResponse(json.dumps({'response': 'db updated'}), content_type='application/json')

    def get_repos_from_API(self, username):
        print('## get_repos_from_API')
        user = github.get_user(username)
        repos = user.get_repos()
        return repos
    
    def update_or_create_github_repos(self, requested_user, repos):
        # upate last_repos_update field
        requested_user.last_repos_update = timezone.now()
        requested_user.save()
        print('## update_or_create_github_repos')
        for repo in repos:
            try:
                new_repo, created = GithubRepo.objects.update_or_create(
                    name=repo.name,
                    owner=requested_user,
                    created_at=repo.created_at + timedelta(hours=9),
                    path=repo.full_name,          
                    defaults={
                        'description': repo.description,
                        'pushed_at': repo.pushed_at + timedelta(hours=9),
                        'homepage': repo.homepage,
                        'number_of_commits': repo.get_commits().totalCount,  
                    }
                )
                print(new_repo, 'created', created)
            except:
                print('## error')
        requested_repos = GithubRepo.objects.filter(
            owner=requested_user
        ).order_by('-pushed_at')
        return requested_repos

class RepoDetailView(View):    
    def get(self, request, *args, **kwargs):
        print('########### RepoDetailView')
        
        # init
        context = {}
        
        # add githubRepo to context
        self.githubRepo = GithubRepo.objects.get(pk=kwargs.get('pk'))
        context['object'] = self.githubRepo        
    
        # add commits to context
        commits_connected = RepoCommit.objects.filter(
            repo_connected=self.githubRepo
        )
        context['commits'] = commits_connected
        
        # add contents to context
        contents_connected = RepoContentFile.objects.filter(
            repo_connected=self.githubRepo
        )
        contents_json = serializers.serialize('json', contents_connected)
        context['contents'] = contents_json
        
        return render(request, 'gitAPI/repo_detail.html', context)

class FileDetailView(View):
    def post(self, request, *args, **kwargs):
        # format requested data
        data = request.POST.dict()
        file_path = data.get('file_path')
        sha = data.get('sha')
        repo_path = data.get('repo_path')
        
        # use Github API to get file contents and decode base64
        repo = github.get_repo(repo_path)
        file_contents = repo.get_git_blob(sha).content
        decoded_file_contents = base64.b64decode(file_contents).decode('utf-8')
        
        # get file comments
        my_repo = GithubRepo.objects.get(path=repo_path)
        my_contentFile = RepoContentFile.objects.get(
            repo_connected=my_repo,
            path=file_path,
        )
        
        file_comments = FileComment.objects.filter(
            repo_connected=my_repo,
            file_connected=my_contentFile,
        ).order_by('-updated')
        
        file_comments_json = serializers.serialize(
            'json', 
            file_comments, 
            fields=('content', 'line_number', 'author', 'updated')   
        )        
        
        context = {
            'data': decoded_file_contents,
            'file_comments': file_comments_json,
        }
        
        return HttpResponse(json.dumps(context), content_type='application/json')

class AddFileCommentView(View):
    def post(self, request, *args, **kwargs):
        # get comment data
        data = request.POST.dict()
        print('## AddFileCommentView')
        print(data)
        
        # get repo and file
        githubRepo = GithubRepo.objects.get(
            path=data.get('repo'),
        )
        repoContentFile = RepoContentFile.objects.get(
            repo_connected=githubRepo,
            sha=data.get('file_sha'),
        )
        
        # create new file comment
        new_file_comment = FileComment(
            repo_connected=githubRepo,
            file_connected=repoContentFile,
            content=data.get('comment'),
            line_number=data.get('line_number') or None,
            author=self.request.user,
        )
        new_file_comment.save()
        
        # get all related file comments
        file_comments = FileComment.objects.filter(
            repo_connected=githubRepo,
            file_connected=repoContentFile,
        )
        file_comments_json = serializers.serialize(
            'json', 
            file_comments, 
            fields=('content', 'line_number', 'author', 'updated')   
        )

        context = {
            'file_comments': file_comments_json,
        }
        
        return HttpResponse(json.dumps(context), content_type='application/json')

class RefreshRepo(View):
    # update repo using github API
    def get(self, request, *args, **kwargs):
        self.githubRepo = GithubRepo.objects.get(pk=kwargs.get('pk'))
        
        # update
        self.update_github_repo()
        self.create_repo_commits()
        self.delete_repo_content_files()
        self.create_repo_content_files()
        return redirect('repo-detail', pk=kwargs.get('pk'))
    
    def update_github_repo(self):
        # get repo info with gitAPI
        new_repo = github.get_repo(self.githubRepo.path)

        # update
        defaults={
            'description': new_repo.description,
            'pushed_at': new_repo.pushed_at + timedelta(hours=9),
            'homepage': new_repo.homepage,
            'number_of_commits': new_repo.get_commits().totalCount,
            'refreshed_at': timezone.now(),
        }
        repo = GithubRepo.objects.get(pk=self.githubRepo.pk)
        for key, val in defaults.items():
            setattr(repo, key, val)
        repo.save()
        print('## github_repo updated')
        
    def create_repo_commits(self):
        # repo
        repo = github.get_repo(self.githubRepo.path)
        
        # commits
        commits = repo.get_commits()
        
        # create
        for commit in commits:
            repoCommit, created = RepoCommit.objects.get_or_create(
                repo_connected=self.githubRepo,
                author=commit.author.login,
                message=commit.commit.message,
                url=commit.url,
                committed_at=commit.commit.committer.date + timedelta(hours=9),
            )
            if created:
                print(f'new commit {commit.url} created!')

    def delete_repo_content_files(self):     
        RepoContentFile.objects.filter(
            repo_connected=self.githubRepo
        ).delete()  
        print(f"{self.githubRepo}'s RepoContentFiles deleted")
    
    def create_repo_content_files(self): 
        # repo
        repo = github.get_repo(self.githubRepo.path)
        
        # contents
        contents = deque(repo.get_contents(''))
        
        # create
        while contents:
            curr_content = contents.popleft()
            if curr_content.type == 'dir':
                for next_content in repo.get_contents(curr_content.path)[::-1]:
                    contents.appendleft(next_content)

            # create regardless of file type
            repoContentFile, created = RepoContentFile.objects.get_or_create(
                repo_connected=self.githubRepo,
                name=curr_content.name,
                path=curr_content.path,
                content_type=curr_content.type,
                url=curr_content.url,
                sha=curr_content.sha,
            )
            if created:
                print(curr_content.path, ' created')
            else:
                print(curr_content.path, ' updated')
