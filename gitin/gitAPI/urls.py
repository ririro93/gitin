from django.contrib import admin
from django.urls import path, include

from .views import (
    CreateGithubRepo,
    RepoDetailView,
)

urlpatterns = [
    path('create-repo-info', CreateGithubRepo.as_view(), name='github'),
    path('repo-detail/<int:pk>/', RepoDetailView.as_view(), name='repo-detail'),
]