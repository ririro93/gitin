import requests
import json
import base64
from pprint import pprint
from github import Github
from collections import deque
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings as django_settings
from django.core import serializers
from django.views import View
from django.views.generic import DetailView, ListView, CreateView
from django.views.generic.edit import FormMixin

from .models import GithubUser, GithubRepo, RepoComment, RepoCommit, RepoContentFile
from .forms import CommentForm

G_TOKEN = django_settings.GITHUB_TOKEN
G_USERNAME = django_settings.GITHUB_USERNAME
github = Github(G_TOKEN)

class SearchGithub(View):    
    def post(self, request, *args, **kwargs):
        # POST request
        search_word = request.POST.get('search_word')
        print('## searching for: ', search_word)
        
        # check if user in db -> return None if not found
        exact_user, github_users = self.get_github_users(search_word)
        
        # check if repo in db -> return None if not found
        exact_repo, github_repos = self.get_github_repos(search_word)
        
        # if exact user not in db check with github API
        if not exact_user and "/" not in search_word:
            exact_user = self.create_github_user(search_word)
        
        # if search_word contains a / check with github API
        
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
        ) or None
        
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
        ) or None
        if "/" in search_word:
            github_repos = GithubRepo.objects.filter(
                path__contains=search_word
            ).exclude(
                path__iexact=search_word
            ) or None
        return exact_repo, github_repos
        
    def create_github_user(self, search_word):
        # use github API to see if username exists and create Github User
        try: 
            new_user = github.get_user(search_word)
            GithubUser.objects.create(
                username=new_user.login,
            )
            exact_user = GithubUser.objects.filter(username=new_user.login)
        except: 
            exact_user = None
        print("## github search user result:", exact_user)
        return exact_user

    def create_github_repos(self, userObj, github_user):
        # get repos
        repos = userObj.get_repos()
        
        # for each repo reate or update GithubRepo
        for repo in repos:
            # create or update GithubRepo -> time is UTC based
            githubRepo, created = GithubRepo.objects.update_or_create(
                name=repo.name,
                owner=github_user,
                created_at=repo.created_at + timedelta(hours=9),
                path=repo.full_name,          
                defaults={
                    'description': repo.description,
                    'pushed_at': repo.pushed_at + timedelta(hours=9),
                    'homepage': repo.homepage,
                    'number_of_commits': repo.get_commits().totalCount,  
                }
            )
            if created:
                print(f'{githubRepo} created!')
            else:
                print(f'{githubRepo} updated!')
        
        # order by updated_at
        results = GithubRepo.objects.filter(
            owner=github_user
        ).order_by('-pushed_at')
        return results
    
    def serializeQs(self, qs):
        if qs:
            return serializers.serialize('json', qs)
        return None
    

class RepoDetailView(View):    
    def get(self, request, *args, **kwargs):
        # init
        context = {}
        try:
            updateRepo = request.GET.updateRepo     # add button to update repo
        except:
            updateRepo = False
        print('###########')
        print('update: ', updateRepo)
        
        # add githubRepo to context
        self.githubRepo = GithubRepo.objects.filter(
            pk=kwargs.get('pk')
        )[0]
        context['object'] = self.githubRepo
        context['repo_path'] = self.githubRepo.path
        
        
        # if update update commits and contents
        if updateRepo:
            # create commits and add to context
            context['commits'] = self.create_repo_commits()
            
            # update contents
            self.delete_repo_content_files()
            contents_connected = self.create_repo_content_files()
            contents_json = serializers.serialize('json', contents_connected)
            context['contents'] = contents_json
        else:
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
            
            # add comments to context
            comments_connected = RepoComment.objects.filter(
                repo_connected=self.githubRepo
            ).order_by('-updated')
            context['comments'] = comments_connected
        
        # check this portion
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        return render(request, 'gitAPI/githubrepo_detail.html', context)
    
    def post(self, request, *args, **kwargs):
        """
        create new RepoComment
        """
        githubRepo = GithubRepo.objects.filter(
            pk=kwargs.get('pk')
        )[0]
        new_comment = RepoComment(
            content=request.POST.get('content'),
            author=self.request.user,
            repo_connected=githubRepo,
        )
        new_comment.save()
        # why return this?
        return self.get(request, *args, **kwargs)
    
    def create_repo_commits(self):
        # repo
        repo = github.get_repo(self.githubRepo.path)
        
        # commits
        commits = repo.get_commits()
        
        # create
        qs = RepoCommit.objects.none()
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
            qs |= RepoCommit.objects.filter(pk=repoCommit.pk)
        return qs

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
        qs = RepoContentFile.objects.none()
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
            print(curr_content.path, ' created')
            qs |= RepoContentFile.objects.filter(pk=repoContentFile.pk)
        return qs
                
                
class FileDetailView(View):
    def post(self, request, *args, **kwargs):
        # format requested data
        data = request.POST.dict()
        sha = data.get('sha')
        repo_path = data.get('repo_path')
        
        # use Github API to get file contents and decode base64
        repo = github.get_repo(repo_path)
        file_contents = repo.get_git_blob(sha).content
        decoded_file_contents = base64.b64decode(file_contents).decode('utf-8')
        context = {
            'data': decoded_file_contents,
        }
        
        return HttpResponse(json.dumps(context), content_type='application/json')