from django.contrib import admin
from django.urls import path, include

from .views import (
    SearchGithub,
    RepoListView,
    RepoDetailView,
)

urlpatterns = [
    path('search-github/', SearchGithub.as_view(), name='search-github'),
    path('search-github/<int:pk>/repo-detail/', RepoDetailView.as_view(), name='repo-detail'),
    path('add/repo-list/', RepoListView.as_view(), name='repo-list'),
]