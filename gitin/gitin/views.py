from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView

class Home_page(TemplateView):
    template_name = 'home_page.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'GitIn'
        context['content'] = 'Welcome to GitIn'
        return context