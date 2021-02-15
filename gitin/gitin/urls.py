from django.contrib import admin
from django.urls import path, include

from .views import (
    Home_page,
)

urlpatterns = [
    path('', Home_page.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),   
    path('github/', include('gitAPI.urls')),
]
