from django.shortcuts import render
from tasties_app.models import Recipe, Rating
from django.db.models import Avg
from collections import OrderedDict
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm


def index(request):
    return render(request, 'tasties_app/index.html',)


def base(request):
    return render(request, 'tasties_app/base.html',)


def recipes(request):
    recipes_list = Recipe.objects.all()
    recipes_with_ratings = {}
    for recipe in recipes_list:
        recipes_with_ratings[recipe] = Rating.objects.filter(recipe_id=recipe).aggregate(Avg('rating'))['rating__avg']
    recipes_with_ratings = OrderedDict(sorted(recipes_with_ratings.items(), key=lambda x: x[1], reverse=True))
    context = {'recipes_with_ratings': recipes_with_ratings}
    return render(request, 'tasties_app/recipes.html', context)


def register(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    
    context = {'form': form}
    return render(request, 'tasties_app/register.html', context)
