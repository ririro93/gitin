import requests
from pprint import pprint
from github import Github
from collections import deque
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.conf import settings as django_settings
from django.views import View
from django.views.generic import DetailView

from .models import GithubUser, GithubRepo, RepoComment, RepoCommit, RepoContentFile
from .forms import CommentForm

G_TOKEN = django_settings.GITHUB_TOKEN
G_USERNAME = django_settings.GITHUB_USERNAME

class CreateGithubRepo(View):
    """
    http://127.0.0.1:8000/github/get-repo-info/?username=ririro93
    여기서 repo이름/commits 들어가면 모든 commit 다 볼 수 있음
    -> commit 수 비례 사이즈 크게 보여주고 싶음
    https://api.github.com/repos/ririro93/algorithm_probs/commits
    """
    def get(self, request):
        # use PyGithub library
        self.g = Github(G_TOKEN)
        self.username = request.GET.get('username')
        
        # GET request
        username = self.username
        URL = f'https://api.github.com/users/{username}/repos'
        res = requests.get(URL, auth=(G_USERNAME, G_TOKEN))
        
        # if username exists -> create or update user and owned repos
        if res.status_code == 200:
            self.create_github_user(res, username)
        return JsonResponse({'githubData' : res.json()}, status = 200)
    
    # there should be a better way to implement these two methods without them being connected
    def create_github_user(self, res, username):
        githubUser, created = GithubUser.objects.update_or_create(
            username=username
        )
        self.create_github_repos(res, githubUser)
    
    def create_github_repos(self, res, githubUser):
        # get GithubRepo field names
        github_repo_fields = list(map(lambda x: x.name, GithubRepo._meta.fields))
        repos = res.json()
        
        # for each repo
        for repo in repos:
            # create or update GithubRepo
            githubRepo, created = GithubRepo.objects.update_or_create(
                **{key: val for key, val in repo.items() if key in github_repo_fields and key not in ['id', 'owner']},
                owner=githubUser
            )
            if created:
                print(f'{githubRepo} added to db')

            # create RepoCommits
            self.create_repo_commits(repo, githubRepo)
            
            # delete former RepoContentFiles and create new
            # self.delete_repo_content_files(repo, githubRepo)
            self.create_repo_content_files(repo, githubRepo)
    
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
                

class AddGithubView():
    pass
        
class RepoDetailView(DetailView):
    
    model = GithubRepo
    
    def get_context_data(self, **kwargs):
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
        print(context)
        return context
    
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