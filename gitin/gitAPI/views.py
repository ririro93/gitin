import requests
from pprint import pprint
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView

from .models import GithubUser, GithubRepo, RepoComment
from .forms import CommentForm

class CreateGithubRepo(View):
    """
    http://127.0.0.1:8000/github/get-repo-info/?username=ririro93
    여기서 repo이름/commits 들어가면 모든 commit 다 볼 수 있음
    -> commit 수 비례 사이즈 크게 보여주고 싶음
    https://api.github.com/repos/ririro93/algorithm_probs/commits
    """
    def get(self, request):
        username = request.GET.get('username')
        URL = f'https://api.github.com/users/{username}/repos'
        res = requests.get(URL)
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
        # gets all the field names from GithubRepo Model
        github_repo_fields = list(map(lambda x: x.name, GithubRepo._meta.fields))
        repos = res.json()
        for repo in repos:
            githubRepo, created = GithubRepo.objects.update_or_create(
                **{key: val for key, val in repo.items() if key in github_repo_fields and key != 'owner'},
                owner=githubUser
            )
            if created:
                print(f'{githubRepo} added to db')
                
                
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
            author=self.request.user.gitinuser,
            repo_connected=self.get_object(),
        )
        new_comment.save()
        # why return this?
        return self.get(self, request, *args, **kwargs)