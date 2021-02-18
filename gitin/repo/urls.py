from django.contrib import admin
from django.urls import path, include

from .views import (
    RepoDetailView,
)

urlpatterns = [
    path('repo-detail/<int:pk>/', RepoDetailView.as_view(), name='repo-detail'),
]