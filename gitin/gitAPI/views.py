import requests
from pprint import pprint
from github import Github
from collections import deque
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings as django_settings
from django.views import View
from django.views.generic import DetailView, ListView, CreateView
from django.views.generic.edit import FormMixin

from .models import GithubUser, GithubRepo, RepoComment, RepoCommit, RepoContentFile
from .forms import CommentForm

G_TOKEN = django_settings.GITHUB_TOKEN
G_USERNAME = django_settings.GITHUB_USERNAME

class SearchGithub(View):    
    def __init__(self):
        self.github = Github(G_TOKEN)
    
    def get(self, request):
        # GET request
        search_word = request.GET.get('search_word')
        
        # if userObj exists -> create or update GithubUser and related GithubRepos
    # try:
        userObj = self.github.get_user(search_word)
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
        
        # # for each repo reate or update GithubRepo
        # for repo in repos:
        #     # create or update GithubRepo -> time is UTC based
        #     githubRepo, created = GithubRepo.objects.update_or_create(
        #         name=repo.name,
        #         owner=github_user,
        #         description=repo.description,
        #         created_at=repo.created_at + timedelta(hours=9),
        #         pushed_at=repo.pushed_at + timedelta(hours=9),
        #         homepage=repo.homepage,
        #         number_of_commits=repo.get_commits().totalCount,            
        #     )
        #     if created:
        #         print(f'{githubRepo} created!')
        #     else:
        #         print(f'{githubRepo} updated!')
        
        # order by updated_at
        results = GithubRepo.objects.filter(
            owner=github_user
        ).order_by('-pushed_at')
        
        return results
    
    def create_repo_commits(self, repo, githubRepo):
        """
        get commits data and create RepoCommit objects
        this only shows the most recent 30 commits
        """
        # get API
        commits_URL = repo.get('commits_url').replace('{/sha}', '')
        commits_res = requests.get(commits_URL, auth=(G_USERNAME, G_TOKEN))
        commits_json = commits_res.json()
        print(f'for {repo.get("name")}')
        
        # for each commit  (testing -> just get 3 commits per repo)
        for commit_json in commits_json[:3]:
            # format
            repo_connected = githubRepo
            commit = commit_json.get('commit')
            url = commit_json.get('url')
            
            # some commits had null as author..
            try:
                author = commit_json.get('author').get('login')
            except:
                author = 'unknown'
            
            # create 
            repo_commit, created = RepoCommit.objects.update_or_create(
                repo_connected=repo_connected,
                author=author,
                commit=commit,
                url=url,
            )
            if created:
                print(f'{repo_commit} added to db')

    def delete_repo_content_files(self, repo, githubRepo):     
        repoContentFiles = repoContentFiles.objects.filter(
            repo_connected=githubRepo
        ).delete()  
        print(f"{githubRepo}'s RepoContentFiles deleted")
    
    def create_repo_content_files(self, repo, githubRepo): 
        # repo
        repo_name = self.username + '/' + repo.get('name')
        repo = self.g.get_repo(repo_name)
        
        # contents
        contents = deque(repo.get_contents(''))
        
        # create 
        while contents:
            curr_content = contents.popleft()
            if curr_content.type == 'dir':
                for next_content in repo.get_contents(curr_content.path)[::-1]:
                    contents.appendleft(next_content)

            # create regardless of file type
            RepoContentFile.objects.create(
                repo_connected=githubRepo,
                path=curr_content.path,
                content_type=curr_content.type,
                url=curr_content.url,
            )
            print(curr_content.path, ' created')
                

class RepoListView(ListView):
    template_name='githubrepo_list.html'
    
    def post(self, request, *args, **kwargs):
        """
        update or create GithubUser and all connected GithubRepos
        """
        new_github_user = GithubUser.objects.update_or_create(
            username=request.POST.get('username')
        )
        self.create_github_repos(res, githubUser)
    
    def get_context_data(self, **kwargs):
        """
        add commits, contents, comments
        """
        context = super().get_context_data(**kwargs)

        # # add repos
        # repo_connected = GithubRepo.objects.filter(
        #     owner=
        # )
        
        print(context)
        return context

class RepoDetailView(DetailView):    
    model = GithubRepo
    
    def post(self, request, *args, **kwargs):
        """
        create new RepoComment
        """
        new_comment = RepoComment(
            content=request.POST.get('content'),
            author=self.request.user,
            repo_connected=self.get_object(),
        )
        new_comment.save()
        # why return this?
        return self.get(self, request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """
        add commits, contents, comments
        """
        context = super().get_context_data(**kwargs)

        # add contents to context
        contents_connected = RepoContentFile.objects.filter(
            repo_connected=self.get_object()
        )
        context['contents'] = contents_connected

        # add commits to context
        commits_connected = RepoCommit.objects.filter(
            repo_connected=self.get_object()
        )
        context['commits'] = commits_connected
        
        # add comments to context
        comments_connected = RepoComment.objects.filter(
            repo_connected=self.get_object()
        ).order_by('-updated')
        context['comments'] = comments_connected
        
        # check this portion
        if self.request.user.is_authenticated:
            # context['comment_form'] = CommentForm(instance=self.request.user)
            context['comment_form'] = CommentForm()
        return context