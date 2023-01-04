from django.shortcuts import render
from tasties_app.models import Recipe, Rating
from django.db.models import Avg


def index(request):
    return render(request, 'tasties_app/index.html',)


def base(request):

    search_input = request.POST.get('search')
    if search_input:
        recipe_object = Recipe.objects.filter(title=search_input)
        if recipe_object:
            return search_recipe(request, search_input)
        else:
            return recipes(request)

    else:
        return render(request, 'tasties_app/base.html')



def recipes(request):
    recipes_list = Recipe.objects.all()
    recipes_with_ratings = {}
    for recipe in recipes_list:
        recipes_with_ratings[recipe] = Rating.objects.filter(recipe_id=recipe).aggregate(Avg('rating'))['rating__avg']

    context = {'recipes_with_ratings': recipes_with_ratings}
    return render(request, 'tasties_app/recipes.html', context)


def search_recipe(request, rsp=None):
    recipes_list = Recipe.objects.filter(title=rsp)
    recipes_with_ratings = {}
    for recipe in recipes_list:
        recipes_with_ratings[recipe] = Rating.objects.filter(recipe_id=recipe).aggregate(Avg('rating'))['rating__avg']

    context = {'recipes_with_ratings': recipes_with_ratings}
    return render(request, 'tasties_app/recipes.html', context)
