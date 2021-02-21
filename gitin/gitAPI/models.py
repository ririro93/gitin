from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class GithubUser(models.Model):
    gitinuser = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    username = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def get_githubrepos(self):
        """
        for showing on admin
        """
        repos = [x for x in self.githubrepo_set.all()]
        return repos
        
    def __str__(self):
        return self.username

class GithubRepo(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey('GithubUser', on_delete=models.CASCADE)
    description = models.CharField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField()
    pushed_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    homepage = models.CharField(max_length=200, blank=True, null=True)
    number_of_commits = models.IntegerField()
    path = models.CharField(max_length=300)
    
    def num_commits(self):
        return RepoCommit.objects.filter(repo_connected=self).count()
    
    def num_comments(self):
        return RepoComment.objects.filter(repo_connected=self).count()

    def __str__(self):
        return self.name
    
class RepoComment(models.Model):
    repo_connected = models.ForeignKey(
        GithubRepo,
        related_name='comments',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='author',
        on_delete=models.CASCADE,
    )
    content = models.CharField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.author} {self.repo_connected} {self.content}'

class RepoCommit(models.Model):
    repo_connected = models.ForeignKey(
        GithubRepo,
        related_name='commits',
        on_delete=models.CASCADE,
    )
    author = models.CharField(max_length=200, blank=True, null=True)
    message = models.CharField(max_length=200)
    url = models.CharField(max_length=300)
    committed_at = models.DateTimeField()
        
    def __str__(self):
        return self.message

class RepoContentFile(models.Model):
    repo_connected = models.ForeignKey(
        GithubRepo,
        related_name='contents',
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=200)
    path = models.CharField(max_length=300)
    content_type = models.CharField(max_length=200)
    url = models.CharField(max_length=300)
    
    def __str__(self):
        return self.path