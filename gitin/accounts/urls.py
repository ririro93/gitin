from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from .views import (
    signup_view,
    login_view,
    logout_view,
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),   
    
    # need to make reset_pw_view
    path('reset_pw/', signup_view, name='reset_pw'),   
]