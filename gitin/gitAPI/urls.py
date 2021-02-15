from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from .views import (
    GithubView,
)

urlpatterns = [
    path('get-repo-info/', GithubView.as_view(), name='github'),
]