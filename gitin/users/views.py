from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

from .forms import SignupForm, LoginForm
from .models import CustomUser

User = get_user_model()

def signup_view(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password1 = form.cleaned_data.get('password1')
        password2 = form.cleaned_data.get('password2')
        try:
            user = User.objects.create_user(email, password1)
            user = authenticate(request, email=email, password=password1)
            print('new user signup!')
        except:
            user = None
            print('INVALID SIGNUP!')
        
        # if valid signup
        if user != None:
            login(request, user)
            return redirect('/')
        # if invalid
        else:
            print('invalid sign up')
            print(request.session)
    return render(request, 'users/signup_page.html', {'form': form})

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        # if valid login
        if user != None:
            login(request, user)
            next_page = request.POST.get('next', '/')
            return redirect(next_page)
        # if invalid
        else:
            pass
            ## 이런 식으로 많이 틀리면 다른데로 보내든가 할 수 있음
            # attempt = request.session.get('attempt', 0)
            # request.session['attempt'] = attempt + 1
            # return redirect('/invalid-password')
            # request.session['invalid_user'] = 1
    return render(request, 'users/login_page.html', {'form': form})

def logout_view(request):
    logout(request)
    next_page = request.GET.get('next', login_view)
    return redirect(next_page)