from django.contrib import admin
from django.urls import path, include

from .views import (
    SearchGithub,
    UserDetailView,
    RepoDetailView,
    FileDetailView,
    AddFileCommentView,
)

urlpatterns = [
    path('search/', SearchGithub.as_view(), name='search'),
    path('search/user-detail/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('search/repo-detail/<int:pk>/', RepoDetailView.as_view(), name='repo-detail'),
    path('search/repo-detail/<int:pk>/get-file/', FileDetailView.as_view(), name='file-detail'),
    path('search/repo-detail/<int:pk>/add-file-comment/', AddFileCommentView.as_view(), name='file-comment'),
]