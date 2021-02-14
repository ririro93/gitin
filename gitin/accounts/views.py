from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .forms import RegisterForm, LoginForm

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password1 = form.cleaned_data.get('password1')
        password2 = form.cleaned_data.get('password2')

        try:
            user = User.objects.create_user(username, email, password)
        except:
            user = None
            
        if user != None:
            login(request, user)
            return redirect('/')
        # if invalid
        else:
            ## 이런 식으로 많이 틀리면 다른데로 보내든가 할 수 있음
            # attempt = request.session.get('attempt', 0)
            # request.session['attempt'] = attempt + 1
            # return redirect('/invalid-password')
            request.session['register_error'] = 1
    return render(request, 'forms.html', {'form': form})

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            return redirect('/')
        # if invalid
        else:
            ## 이런 식으로 많이 틀리면 다른데로 보내든가 할 수 있음
            # attempt = request.session.get('attempt', 0)
            # request.session['attempt'] = attempt + 1
            # return redirect('/invalid-password')
            request.session['invalid_user'] = 1
    return render(request, 'forms.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/login')