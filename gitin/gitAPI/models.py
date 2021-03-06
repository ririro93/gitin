from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class GithubUser(models.Model):
    gitinuser = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    username = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    last_repos_update = models.DateTimeField(null=True, blank=True)
    
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
    refreshed_at = models.DateTimeField(blank=True, null=True)
    homepage = models.CharField(max_length=200, blank=True, null=True)
    number_of_commits = models.IntegerField()
    path = models.CharField(max_length=300)
    
    def num_commits(self):
        return RepoCommit.objects.filter(repo_connected=self).count()
    
    def num_comments(self):
        return RepoComment.objects.filter(repo_connected=self).count()

    def __str__(self):
        return self.name

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
    sha = models.CharField(max_length=200)
    
    def __str__(self):
        return self.path
    
class FileComment(models.Model):
    repo_connected = models.ForeignKey(
        GithubRepo,
        related_name='file_comments',
        on_delete=models.CASCADE,
    )
    file_connected = models.ForeignKey(
        RepoContentFile,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='file_comments',
        on_delete=models.CASCADE,
    )
    line_number = models.IntegerField(blank=True, null=True)
    content = models.CharField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} {self.repo_connected} {self.content}'