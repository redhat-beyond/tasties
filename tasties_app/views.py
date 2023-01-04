from django.shortcuts import render
from tasties_app.models import Recipe, Rating
from django.db.models import Avg
from collections import OrderedDict


def index(request):
    return render(request, 'tasties_app/index.html',)


def base(request):
    search_input = request.POST.get('search')
    if search_input:
        return recipes(request, search_input)
    else:
        return render(request, 'tasties_app/base.html')


def recipes(request, search_value=None):
    recipes_list = Recipe.objects.filter(title__icontains=search_value)
    if recipes_list:
        recipes_with_ratings = {}
        for recipe in recipes_list:
            recipes_with_ratings[recipe] = Rating.objects.filter(recipe_id=recipe).aggregate(Avg('rating'))
            ['rating__avg']
            recipes_with_ratings = OrderedDict(sorted(recipes_with_ratings.items(), key=lambda x: x[1], reverse=True))
        context = {'recipes_with_ratings': recipes_with_ratings}
        return render(request, 'tasties_app/recipes.html', context)
    else:
        recipes_list = Recipe.objects.all()
        recipes_with_ratings = {}
        for recipe in recipes_list:
            recipes_with_ratings[recipe] = Rating.objects.filter(recipe_id=recipe).aggregate(Avg('rating'))
            ['rating__avg']
            recipes_with_ratings = OrderedDict(sorted(recipes_with_ratings.items(), key=lambda x: x[1], reverse=True))
        context = {'recipes_with_ratings': recipes_with_ratings}
        return render(request, 'tasties_app/recipes.html', context)
