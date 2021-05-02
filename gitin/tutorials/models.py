from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
from gitAPI.models import GithubRepo

class Tutorial(models.Model):
    githubRepo = models.ForeignKey(GithubRepo, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to='uploads/tutorial_thumbnail/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author.email} {self.githubRepo.name}'