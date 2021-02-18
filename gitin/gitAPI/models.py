from django.db import models
from accounts.models import GitinUser

class GithubUser(models.Model):
    gitinuser = models.OneToOneField(GitinUser, on_delete=models.SET_NULL, null=True)
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
    html_url = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    pushed_at = models.DateTimeField()
    homepage = models.CharField(max_length=200, blank=True, null=True)
    
    def get_number_of_comments(self):
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
        GitinUser,
        related_name='author',
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.author} {self.repo_connected} {self.content}'
    

        
    