from django.shortcuts import render, redirect
from tasties_app.models import Recipe, Rating, Comment
from django.db.models import Avg
from collections import OrderedDict
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from django.contrib import messages
from django.utils import timezone


def base(request):
    return render(request, 'tasties_app/base.html',)


@login_required(login_url='login')
def recipes(request):
    recipes_list = Recipe.objects.all()
    recipes_with_ratings = {}
    for recipe in recipes_list:
        recipes_with_ratings[recipe] = Rating.objects.filter(recipe_id=recipe).aggregate(Avg('rating'))['rating__avg']
    recipes_with_ratings = OrderedDict(sorted(recipes_with_ratings.items(), key=lambda x: x[1], reverse=True))
    context = {'recipes_with_ratings': recipes_with_ratings}
    return render(request, 'tasties_app/recipes.html', context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Username OR password is incorrect')
    return render(request, 'tasties_app/login.html',)


def logout_user(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.user.is_authenticated:
        return redirect('recipes')

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
        else:
            for error_message in form.errors.values():
                messages.error(request, error_message)

    context = {'form': form}
    return render(request, 'tasties_app/register.html', context)


@login_required(login_url='login')
def view_recipe(request, recipe_id=None):
    if not Recipe.objects.filter(pk=recipe_id).exists():
        return redirect('recipes')
    recipe = Recipe.objects.get(pk=recipe_id)
    ingredients = recipe.ingredient_set.all()
    rating = recipe.rating_set.aggregate(Avg('rating'))['rating__avg']
    categories = recipe.categories.all()
    if request.method == 'POST':
        add_comment(request, recipe.title)
    comments = Comment.objects.filter(recipe_id=recipe.id)
    context = {'recipe': recipe, 'ingredients': ingredients, 'rating': rating,
               'categories': categories, 'comments': comments}
    return render(request, 'tasties_app/view_recipe.html', context)


@login_required(login_url='login')
def add_comment(request, recipe_title):
    comment_value = request.POST.get('comment-adding')
    recipe = Recipe.objects.get(title=recipe_title)
    user = request.user
    comment_input = Comment(author_id=user, recipe_id=recipe, publication_date=timezone.now(),
                            comment_text=comment_value)
    comment_input.save()