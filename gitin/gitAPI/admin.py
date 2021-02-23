from django.contrib import admin

from .models import GithubUser, GithubRepo, RepoComment, RepoCommit, RepoContentFile
 
    
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

@admin.register(RepoComment)
class RepoCommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'updated'
    list_display = (
        'repo_connected',
        'author',
        'content',
        'created',
        'updated',
    )


@admin.register(RepoCommit)
class RepoCommitAdmin(admin.ModelAdmin):
    # date_hierarchy = 'updated'
    list_display = (
        'repo_connected',
        'author',
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