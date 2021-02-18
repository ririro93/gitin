from django.contrib import admin

from .models import GithubUser, GithubRepo, RepoComment
 
    
@admin.register(GithubUser)
class GithubUserAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = (
        'username',
        'get_githubrepos',
        'created',
        'updated',
    )
    readonly_fields = ['created', 'updated']
    
    
@admin.register(GithubRepo)
class GithubRepoAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated_at'
    list_display = (
        'pk',
        'name',
        'owner',
        'get_number_of_comments',
        'description',
        'created_at', 
        'updated_at', 
        'pushed_at',
    )

@admin.register(RepoComment)
class RepoCommentsAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = (
        'repo_connected',
        'author',
        'content',
        'created',
        'updated',
    )