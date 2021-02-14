from django import forms
from django.contrib.auth import get_user_model

# check for unique email and username
User = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'user-id'
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'id': 'user-email'
            }
        )
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'user-password'
            }
        ),
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'user-confirm-password'
            }
        ),
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # iexact -> not case-sensitive
        qs = User.objects.filter(username__iexact=username)
        if qs.exists():
            raise forms.ValidationError('This is an invalid username, please pick another')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # iexact -> not case-sensitive
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError('This email is already in use, please pick another')
        return email
    

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'user-id'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'user-password'
            }
        ),
    )
    
    # def clean(self):
    #     username = self.cleaned_data.get('username')
    #     password = self.cleaned_data.get('password')
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # iexact -> not case-sensitive
        qs = User.objects.filter(username__iexact=username)
        if not qs.exists():
            raise forms.ValidationError('This is an invalid username.')
        return username