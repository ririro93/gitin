from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from .views import (
    register_view,
    login_view,
    logout_view,
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    
    # sns logins
    path('login/google_login/', TemplateView.as_view(template_name='accounts/google_login.html')),
]