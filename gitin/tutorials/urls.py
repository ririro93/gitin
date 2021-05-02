from django.urls import path, include
from .views import TutorialListView

app_name = 'tutorials'

urlpatterns = [
    path('', TutorialListView.as_view(), name='tutorial_list'),
]