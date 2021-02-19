import requests
from pprint import pprint
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from .models import GithubUser, GithubRepo, RepoComment, RepoCommit
from .forms import CommentForm

class CreateGithubRepo(View):
    """
    http://127.0.0.1:8000/github/get-repo-info/?username=ririro93
    여기서 repo이름/commits 들어가면 모든 commit 다 볼 수 있음
    -> commit 수 비례 사이즈 크게 보여주고 싶음
    https://api.github.com/repos/ririro93/algorithm_probs/commits
    """
    def get(self, request):
        # GET request
        username = request.GET.get('username')
        URL = f'https://api.github.com/users/{username}/repos'
        res = requests.get(URL)
        
        # if username exists -> create or update user and owned repos
        if res.status_code == 200:
            self.create_github_user(res, username)
        return JsonResponse({'githubData' : res.json()}, status = 200)
    
    # there should be a better way to implement these two methods without them being connected
    def create_github_user(self, res, username):
        githubUser, created = GithubUser.objects.update_or_create(
            username=username
        )
        self.create_github_repo(res, githubUser)
    
    def create_github_repo(self, res, githubUser):
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
    
    def create_repo_commits(self, repo, githubRepo):
        """
        get commits data and create RepoCommit objects
        this only shows the most recent 30 commits
        """
        # get API
        commits_URL = repo.get('commits_url').replace('{/sha}', '')
        commits_res = requests.get(commits_URL)
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


    def create_content(self, repo):
        contents_URL = repo.get('contents_url').replace('{/sha}', '')
        
                
                
class RepoDetailView(DetailView):
    
    model = GithubRepo
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # add comments to context
        comments_connected = RepoComment.objects.filter(
            repo_connected=self.get_object()
        ).order_by('-updated')
        context['comments'] = comments_connected
        
        # check this portion
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm(instance=self.request.user)
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