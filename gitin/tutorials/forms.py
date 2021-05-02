from django.forms import ModelForm

from .models import Tutorial

class TutorialForm(ModelForm):
    class Meta():
        model = Tutorial
        exclude = ['githubRepo', 'author']
