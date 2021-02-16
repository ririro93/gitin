from django.db import models

class GithubUser(models.Model):
    username = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username

class GithubRepo(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey('GithubUser', on_delete=models.CASCADE)
    html_url = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True, null=True)
    # contributors
    # commits
    # contents
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    pushed_at = models.DateTimeField()
    homepage = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

        
    