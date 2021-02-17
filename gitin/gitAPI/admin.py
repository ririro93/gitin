from django.contrib import admin

from .models import GithubUser, GithubRepo
 
    
@admin.register(GithubUser)
class GithubUserAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = (
        'username',
        'created',
        'updated',
    )
    readonly_fields = ['created', 'updated']
    
    
@admin.register(GithubRepo)
class GithubRepoAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated_at'
    list_display = (
        'name',
        'owner',
        'description',
        'created_at', 
        'updated_at', 
        'pushed_at',
    )