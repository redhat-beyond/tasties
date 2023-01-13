from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Recipe


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


class CreateRecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['author_id', 'title', 'description', 'categories', 'directions', 'minutes_to_make']
        widgets = {'author_id': forms.HiddenInput()}
