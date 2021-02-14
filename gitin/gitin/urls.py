from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from .views import (
    Home_page,
)

from accounts.views import (
    login_view,
    logout_view,
    register_view,
)

urlpatterns = [
    path('home', Home_page.as_view()),
    path('admin/', admin.site.urls),
    
    path('login/', login_view),
    path('logout/', logout_view),
    path('register/', register_view),
    
    # allauth test
    path('accounts/', include('allauth.urls')),
    path('', TemplateView.as_view(template_name='social_app/index.html')),

]
