from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Recipe, Category


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
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    # ingredients = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control'}))
    directions = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    minutes_to_make = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    categories = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple(attrs={'class': 'category-select'}),
                                                queryset=Category.objects.all())

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'categories', 'directions', 'minutes_to_make', 'recipe_picture']
        widgets = {'author_id': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super(CreateRecipeForm, self).__init__(*args, **kwargs)
        self.fields['recipe_picture'].required = False
        self.fields['recipe_picture'].upload_to = 'images'
