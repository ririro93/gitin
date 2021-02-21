import requests
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
    def get(self, request):
        # GET request
        search_word = request.GET.get('search_word')
        
        # if userObj exists -> create or update GithubUser and related GithubRepos
    # try:
        userObj = github.get_user(search_word)
        github_user = self.create_github_user(userObj)
        github_repos = self.create_github_repos(userObj, github_user)
        context = {
            'search_word': search_word,
            'github_user': github_user,
            'github_repos': github_repos,
        }
        return render(request, 'gitAPI/search_github.html', context)
    # except:
        
    
    def create_github_user(self, userObj):
        github_user, created = GithubUser.objects.update_or_create(
            username=userObj.login
        )
        if created:
            print(f'{github_user} created!')
        else:
            print(f'{github_user} updated!')
        return github_user
    
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
        
        # if update update commits and contents
        if updateRepo:
            # create commits and add to context
            context['commits'] = self.create_repo_commits()
            
            # update contents
            self.delete_repo_content_files()
            context['contents'] = self.create_repo_content_files()
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
            )
            print(curr_content.path, ' created')
            qs |= RepoContentFile.objects.filter(pk=repoContentFile.pk)
        return qs
                
