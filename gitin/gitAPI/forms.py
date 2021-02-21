from django import forms

from .models import RepoComment

class CommentForm(forms.ModelForm):
    class Meta:
        model = RepoComment
        fields = ['content']
        labels = {
            'content': False,
        }
        widgets = {
            'content': forms.TextInput(
                attrs={
                    'placeholder': 'Write a comment...'
                }
            )
        }