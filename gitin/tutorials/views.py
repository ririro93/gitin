from django.shortcuts import render
from django.views import View

from .models import Tutorial

# Create your views here.
class TutorialListView(View):
    def get(self, request, *args, **kwargs):
        """
        return list of all tutorials available with the desired tag
        """
        tutorials = Tutorial.objects.all()
        context = {
            "tutorials": tutorials,
        }
        return render(request, 'tutorials/tutorial_list.html', context)