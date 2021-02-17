from django.contrib import admin
from .models import GitinUser

@admin.register(GitinUser)
class GitinUserAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'profilename',
    )
   