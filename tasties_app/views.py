from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from tasties_app.models import Recipe, Comment, Category
from django.db.models import Avg
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from django.contrib import messages
from django.utils import timezone


def base(request):
    return render(
        request,
        "tasties_app/base.html",
    )


@login_required(login_url="login")
def recipes(request):
    recipes_list = Recipe.objects.annotate(
        recipe_rating=Avg("rating__rating")
    ).order_by("-recipe_rating")
    categories_list = Category.objects.all()
    selected_category = request.GET.get("category")
    if selected_category:
        if selected_category == "remove_filter":
            return redirect("recipes")
        try:
            category = Category.objects.get(category_name=selected_category)
        except ObjectDoesNotExist:
            return redirect("recipes")
        recipes_list = (
            Category.get_recipes_by_category(category)
            .annotate(recipe_rating=Avg("rating__rating"))
            .order_by("-recipe_rating")
        )
    context = {
        "recipes_list": recipes_list,
        "categories_list": categories_list,
    }
    return render(request, "tasties_app/recipes.html", context)


def login_user(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.info(request, "Username OR password is incorrect")
    return render(
        request,
        "tasties_app/login.html",
    )


def logout_user(request):
    logout(request)
    return redirect("login")


def register(request):
    if request.user.is_authenticated:
        return redirect("index")

    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, "Account was created for " + username)
            return redirect("login")
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
    if request.method == "POST" and request.POST['action'] == 'Comment':
        add_comment(request, recipe)
    comments = recipe.comment_set.all()
    context = {'recipe': recipe, 'ingredients': ingredients, 'rating': rating,
               'categories': categories, 'comments': comments}
    return render(request, 'tasties_app/view_recipe.html', context)


@login_required(login_url='login')
def add_comment(request, recipe):
    comment_value = request.POST.get('comment-adding')
    user = request.user
    comment_input = Comment(author_id=user, recipe_id=recipe, publication_date=timezone.now(),
                            comment_text=comment_value)
    comment_input.full_clean()
    comment_input.save()
