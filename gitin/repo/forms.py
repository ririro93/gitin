from django import forms
from gitAPI.models import RepoComment

class CommentForm(forms.ModelForm):
    class Meta:
        model = RepoComment
        fields = ['content']