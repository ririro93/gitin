from django.contrib import admin
from django.urls import path, include

from .views import (
    SearchGithub,
    RepoListView,
    RepoDetailView,
)

urlpatterns = [
    path('search-github', SearchGithub.as_view(), name='search-github'),
    path('add/repo-list/', RepoListView.as_view(), name='repo-list'),
    path('repo-detail/<int:pk>/', RepoDetailView.as_view(), name='repo-detail'),
]