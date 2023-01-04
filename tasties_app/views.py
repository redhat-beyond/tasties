from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import redirect, render
from tasties_app.models import Category, Recipe, Comment, Ingredient, Rating
from tasties_app.forms import CreateUserForm, CreateRecipeForm
from django.core.exceptions import ObjectDoesNotExist
from django.forms import inlineformset_factory


def base(request):
    return render(
        request,
        "tasties_app/base.html",
    )


@login_required(login_url="login")
def recipes(request, temp=None):
    if temp is None:
        recipes_list = Recipe.objects.annotate(
                                               recipe_rating=Avg("rating__rating")
                                            ).order_by(sort_list(request))
    else:
        if temp == "Empty":
            recipes_list = []
        else:
            recipes_list = temp
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
            .order_by(sort_list(request))
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
    if request.method == "POST" and request.POST.get('action') == 'Add Rating':
        add_rating(request, recipe)
    rating = recipe.rating_set.aggregate(Avg('rating'))['rating__avg']
    categories = recipe.categories.all()
    if request.method == "POST" and request.POST.get('action') == 'Comment':
        add_comment(request, recipe)
    comments = recipe.comment_set.all()
    context = {'recipe': recipe, 'ingredients': ingredients, 'rating': rating,
               'categories': categories, 'comments': comments}
    if recipe.author_id == request.user:
        context['can_edit'] = True
    return render(request, 'tasties_app/view_recipe.html', context)


def sort_list(request):
    if request.method == 'POST' and request.POST.get('action') == 'Sort':
        sort_by = request.POST['sort_by']
        if sort_by == 'date':
            return "-publication_date"
        elif sort_by == 'name':
            return "title"
        else:
            return "-recipe_rating"
    else:
        return "-recipe_rating"


@login_required(login_url='login')
def add_comment(request, recipe):
    comment_value = request.POST.get('comment-adding')
    user = request.user
    comment_input = Comment(author_id=user, recipe_id=recipe, comment_text=comment_value)
    comment_input = Comment(author_id=user, recipe_id=recipe,
                            comment_text=comment_value)
    comment_input.full_clean()
    comment_input.save()


def add_rating(request, recipe):
    rating_value = request.POST.get('rating')
    if recipe.rating_set.filter(author_id=request.user).exists():
        current_rating = recipe.rating_set.get(author_id=request.user)
        current_rating.rating = int(rating_value)
        current_rating.save()
    else:
        new_rating = Rating(author_id=request.user, recipe_id=recipe, rating=rating_value)
        new_rating.full_clean()
        new_rating.save()


@login_required(login_url='login')
def create_recipe(request):
    recipe = Recipe(author_id=request.user)
    IngredientFormSet = inlineformset_factory(Recipe,
                                              Ingredient,
                                              fields=('description', 'measurement_unit', 'amount'),
                                              min_num=1,
                                              validate_min=True,
                                              extra=9)

    if request.method == 'POST':
        recipe_form = CreateRecipeForm(request.POST, request.FILES, instance=recipe)
        ingredient_formset = IngredientFormSet(request.POST, instance=recipe)
        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            if ingredient_formset.is_valid():
                recipe = recipe_form.save()
                ingredient_formset.save()
                return redirect(f'/view_recipe/{recipe.id}/')
            else:
                for ingredient_form_errors in ingredient_formset.errors:
                    for error_message in ingredient_form_errors.values():
                        messages.error(request, error_message)
        else:
            for error_message in recipe_form.errors.values():
                messages.error(request, error_message)
    else:
        recipe_form = CreateRecipeForm(instance=recipe)
        ingredient_formset = IngredientFormSet(instance=recipe)

    context = {'recipe_form': recipe_form, 'ingredient_formset': ingredient_formset}
    return render(request, 'tasties_app/create_recipe.html', context)


@login_required(login_url='login')
def edit_recipe(request, recipe_id):
    if not Recipe.objects.filter(pk=recipe_id).exists():
        return redirect('recipes')
    recipe = Recipe.objects.get(pk=recipe_id)
    if not recipe.author_id.id == request.user.id:
        return redirect('recipes')
    IngredientFormSet = inlineformset_factory(Recipe,
                                              Ingredient,
                                              fields=('description', 'measurement_unit', 'amount'),
                                              min_num=1,
                                              validate_min=True,
                                              extra=9)

    if request.method == 'POST':
        recipe_form = CreateRecipeForm(request.POST, request.FILES, instance=recipe)
        ingredient_formset = IngredientFormSet(request.POST, instance=recipe)
        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            if ingredient_formset.is_valid():
                recipe = recipe_form.save()
                if not recipe.recipe_picture:
                    recipe.recipe_picture = 'images/tasties_logo_round.png'
                    recipe.save()
                ingredient_formset.save()
                return redirect(f'/view_recipe/{recipe.id}/')
            else:
                for ingredient_form_errors in ingredient_formset.errors:
                    for error_message in ingredient_form_errors.values():
                        messages.error(request, error_message)
        else:
            for error_message in recipe_form.errors.values():
                messages.error(request, error_message)
    else:
        recipe_form = CreateRecipeForm(instance=recipe)
        ingredient_formset = IngredientFormSet(instance=recipe)

    context = {'recipe_form': recipe_form, 'ingredient_formset': ingredient_formset}
    return render(request, 'tasties_app/edit_recipe.html', context)


@login_required(login_url='login')
def recipes_search(request):
    recipes_list = None
    if request.method == 'POST':
        search_value = request.POST.get('search')
        if search_value:
            recipes_list = Recipe.objects.filter(title__icontains=search_value)
        else:
            recipes_list = "Empty"
    return recipes(request, recipes_list)
