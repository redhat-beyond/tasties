from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(max_length=16, widget=forms
                                .PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=16, widget=forms
                                .PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Confirm'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.fields.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.fields.EmailInput(attrs={'class': 'form-control', 'placeholder': 'john@doe.com'}),
        }
