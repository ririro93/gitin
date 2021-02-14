from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from .views import (
    Home_page,
)

from accounts.views import (
    login_view,
    logout_view,
    register_view,
)

urlpatterns = [
    path('', Home_page.as_view()),
    path('admin/', admin.site.urls),
    
    path('login/', login_view),
    path('logout/', logout_view),
    path('register/', register_view),
    
    # allauth test
    path('accounts/', include('allauth.urls')),
]
