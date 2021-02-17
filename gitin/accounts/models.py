from django.db import models
from django.contrib.auth.models import User

class GitinUser(models.Model):
    """
    this class extends the default User model 
    to provide non-auth related data
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profilename = models.CharField(max_length=100)
    profile_img = models.ImageField(upload_to='uploads/profile_img/', null=True, blank=True)
    
    def __str__(self):
        return self.profilename