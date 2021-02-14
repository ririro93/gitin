from django.contrib import admin
from django.urls import path, include

from .views import (
    Home_page,
)

urlpatterns = [
    path('', Home_page.as_view()),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    
    # # allauth test
    # path('accounts/', include('allauth.urls')),
    # path('', TemplateView.as_view(template_name='social_app/index.html')),
]
