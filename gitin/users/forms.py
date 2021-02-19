from django import forms
from django.contrib.auth import get_user_model

# check for unique email and username
User = get_user_model()

class SignupForm(forms.Form):
    email = forms.EmailField(
        label=False,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'id': 'user-email',
                'placeholder': 'Email'
            }
        )
    )
    username = forms.CharField(
        label=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'user-id',
                'placeholder': 'Username'
            }
        )
    )
    password1 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'user-password',
                'placeholder': 'Password'
            }
        ),
    )
    password2 = forms.CharField(
        label=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'user-confirm-password',
                'placeholder': 'Confirm Password'
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # iexact -> not case-sensitive
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError('This email is already in use, please pick another')
        return email
    

class LoginForm(forms.Form):
    email = forms.CharField(
        label=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'user-id',
                'placeholder': 'Email',
            }
        )
    )
    password = forms.CharField(
        label=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'user-password',
                'placeholder': 'Password',
            }
        ),
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # iexact -> not case-sensitive
        qs = User.objects.filter(email__iexact=email)
        if not qs.exists():
            raise forms.ValidationError('This is an invalid email.')
        return email