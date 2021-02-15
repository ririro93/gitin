import requests
from django.http import HttpResponse, JsonResponse
from django.views import View

class GithubView(View):
    """
    http://127.0.0.1:8000/github/get-repo-info/?username=ririro93
    여기서 repo이름/commits 들어가면 모든 commit 다 볼 수 있음
    -> commit 수 비례 사이즈 크게 보여주고 싶음
    https://api.github.com/repos/ririro93/algorithm_probs/commits
    """
    def get(self, request):
        username = request.GET.get('username')
        URL = f'https://api.github.com/users/{username}/repos'
        res = requests.get(URL)
        return JsonResponse({'githubData' : res.json()}, status = 200)