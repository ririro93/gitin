from django.shortcuts import render
from django.views.generic import DetailView

from gitAPI.models import GithubRepo, RepoComment
from .forms import CommentForm

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
            
        return context
    
    def post(self, request, *args, **kwargs):
        new_comment = RepoComment(
            content=request.POST.get('content'),
            author=self.request.user.gitinuser,
            repo_connected=self.get_object(),
        )
        new_comment.save()
        # why return this?
        return self.get(self, request, *args, **kwargs)