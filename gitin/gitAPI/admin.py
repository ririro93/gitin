from django.contrib import admin

from .models import (
    GithubUser, 
    GithubRepo, 
    RepoCommit,
    RepoContentFile,
    FileComment,
)
    
@admin.register(GithubUser)
class GithubUserAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = (
        'pk',
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
        'num_commits',
        'num_comments',
        'description',
        'created_at', 
        'updated_at', 
        'pushed_at',
    )


@admin.register(RepoCommit)
class RepoCommitAdmin(admin.ModelAdmin):
    date_hierarchy = 'committed_at'
    list_display = (
        'repo_connected',
        'author',
        'committed_at',
        'url',
    )

@admin.register(RepoContentFile)
class RepoContentFileAdmin(admin.ModelAdmin):
    list_display = (
        'repo_connected',
        'name',
        'path',
        'url',
    )
    
@admin.register(FileComment)
class FileCommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = (
        'repo_connected',
        'file_connected',
        'line_number',
        'author',
        'content',
        'created',
        'updated',
    )