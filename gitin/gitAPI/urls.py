from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from .views import (
    CreateGithubRepo,
)

urlpatterns = [
    path('create-repo-info', CreateGithubRepo.as_view(), name='github'),
]