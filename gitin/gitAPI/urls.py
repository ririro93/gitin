from django.contrib import admin
from django.urls import path, include

from .views import (
    SearchGithub,
    RepoDetailView,
    FileDetailView,
)

urlpatterns = [
    path('search-github/', SearchGithub.as_view(), name='search-github'),
    path('search-github/<int:pk>/repo-detail/', RepoDetailView.as_view(), name='repo-detail'),
    path('search-github/<int:pk>/repo-detail/get-file/', FileDetailView.as_view(), name='file-detail'),
]