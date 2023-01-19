import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from tasties_app.models import Category, Ingredient, Rating, Recipe, Comment
from authConstants import VALID_USER, VALID_PASSWORD, VALID_EMAIL


@pytest.fixture
def comment():
    """
    in this generate function we create User, Category and Recipe
    objects to fill Comment class and used to test
    """

    user = User.objects.create_user(username="test_user", password="password")
    recipe = Recipe(
        title="Test Recipe1",
        author_id=user,
        description="Test Description1",
        directions="Test Directions1",
        publication_date=timezone.now(),
        minutes_to_make=1,
        recipe_picture="recipe.jpeg",
    )
    recipe.clean_fields()
    recipe.save()
    comment = Comment(
        author_id=user,
        recipe_id=recipe,
        publication_date=timezone.now(),
        comment_text="test comment",
    )
    comment.clean_fields()
    comment.save()

    return comment


@pytest.fixture()
def recipes():
    """
    This fixture generates some test Recipes

    Returns:
        tuple<Recipe>: A number of Recipe test objects
    """
    user = User.objects.create_user(
        "testuser1", "password"
    )  # This is required to create Recipes
    recipe_1 = Recipe(
        title="Test Recipe1",
        author_id=user,
        description="Test Description1",
        directions="Test Directions1",
        minutes_to_make=1,
        recipe_picture="test_picture1",
    )
    recipe_1.save()
    recipe_2 = Recipe(
        title="Test Recipe2",
        author_id=user,
        description="Test Description2",
        directions="Test Directions2",
        minutes_to_make=1,
        recipe_picture="test_picture2",
    )
    recipe_2.save()
    return (recipe_1, recipe_2)


@pytest.fixture()
def categories():
    """
    This fixture generates some test Categories

    Returns:
        tuple<Category>: A number of Category test objects
    """
    category_1 = Category.objects.create(category_name="1")
    category_2 = Category.objects.create(category_name="2")
    category_3 = Category.objects.create(category_name="3")
    return (category_1, category_2, category_3)


@pytest.fixture()
def categorized_recipes(recipes, categories):
    """
    This fixture assigns Categories to Recipes

    Args:
        recipes (fixture): fixture 'recipes'
        categories (fixture): fixture 'categories'

    Returns:
        tuple<tuple<Recipe>, tuple<Category>>: The Recipes generated by 'recipes' assigned with
                       Categories generated by 'categories', as well as the Categories themselves
    """
    recipes[0].categories.add(categories[0])
    recipes[0].categories.add(categories[1])
    recipes[1].categories.add(categories[1])
    return recipes, categories


# ---------------------------------------------------#


@pytest.fixture
def ingredient():
    """
    Creates a user, a recipes, and an ingredient,
    and adds them to the database.
    returns: ingredient
    """
    user1 = User.objects.create_user("test_user", "password")
    category = Category.objects.create(category_name="Breakfast")
    category.save()
    recipe = Recipe(
        title="Test Recipe1",
        author_id=user1,
        description="Test Description1",
        directions="Test Directions1",
        minutes_to_make=1,
        recipe_picture="test_picture1",
    )
    recipe.save()
    recipe.categories.add(category)
    ingredient = Ingredient(
        recipe_id=recipe,
        amount=1.0,
        measurement_unit="WHOLE",
        description="test ingredient",
    )
    ingredient.save()
    return ingredient


@pytest.fixture()
def rating():
    """
    This fixture create the data we need in order to execute the tests.
    """
    user1 = User.objects.create_user("testuser1", "password")
    recipe = Recipe(
        title="Test Recipe1",
        author_id=user1,
        description="Test Description1",
        directions="Test Directions1",
        minutes_to_make=1,
        recipe_picture="test_picture2",
    )
    recipe.save()

    rating = Rating(author_id=user1, recipe_id=recipe, rating=3)
    rating.save()
    return rating


@pytest.fixture
def recipe():
    """
    This fixture create the data we need for tests
    and save it in the data base.
    """
    user1 = User.objects.create_user(username="john", password="password")
    test_data = [
        "Test Recipe1",
        user1,
        "Test Description1",
        "Test Directions1",
        1,
        "test_picture1",
    ]
    category1 = Category.objects.create(category_name="1")
    recipe1 = Recipe(
        title=test_data[0],
        author_id=test_data[1],
        description=test_data[2],
        directions=test_data[3],
        publication_date=timezone.now(),
        minutes_to_make=test_data[4],
        recipe_picture=test_data[5],
    )
    recipe1.full_clean()
    category1.full_clean()
    category1.save()
    recipe1.save()
    recipe1.categories.add(category1)
    recipe1.save()
    return recipe1


@pytest.fixture
def signed_up_credentials():
    user = User.objects.create_user(
        username=VALID_USER, email=VALID_EMAIL, password=VALID_PASSWORD
    )
    user.save()


@pytest.fixture()
def login_to_site(client):
    client.post('/login/', data={'username': VALID_USER, 'password': VALID_PASSWORD})


@pytest.fixture
def recipe_test():
    """
    This fixture create a recipe for test the recipe_view and the add_comment methods.
    """
    user1 = User.objects.create_user(username="username", password="password")
    test_data = [
        "TestRecipe1",
        user1,
        "TestDescription1",
        "TestDirections1",
        1,
        "TestPicture1",
    ]
    category1 = Category.objects.create(category_name="15")
    recipe1 = Recipe(
        title=test_data[0],
        author_id=test_data[1],
        description=test_data[2],
        directions=test_data[3],
        publication_date=timezone.now(),
        minutes_to_make=test_data[4],
        recipe_picture=test_data[5],
    )
    recipe1.full_clean()
    category1.full_clean()
    category1.save()
    recipe1.save()
    recipe1.categories.add(category1)
    recipe1.save()
    return recipe1


@pytest.fixture()
def form_data():
    """
    This fixture creates raw recipe form data to be passed
    by POST request when testing recipe creation

    Returns:
        dictionary: recipe raw data
    """
    form_data = {
        "title": "Valid title",
        "description": "Valid description",
        "directions": "Valid directions",
        "minutes_to_make": 1,
        "categories": {1, 2},
    }
    return form_data


@pytest.fixture()
def formset_data():
    """
    This fixture creates raw ingredient formset data to be passed
    by POST request when testing recipe creation

    Returns:
        _type_: _description_
    """
    formset_data = {
            "ingredient_set-TOTAL_FORMS": 10,
            "ingredient_set-INITIAL_FORMS": 0,
            "ingredient_set-MIN_NUM_FORMS": 1,
            "ingredient_set-MAX_NUM_FORMS": 1000,
            "ingredient_set-0-description": "Valid Ingredient",
            "ingredient_set-0-measurement_unit": "Whole",
            "ingredient_set-0-amount": 1,
            "ingredient_set-0-id": 1,
    }
    for i in range(1, 10):
        formset_data["ingredient_set-" + str(i) + "-description"] = "Valid Ingredient"
        formset_data["ingredient_set-" + str(i) + "-measurement_unit"] = "Whole"
        formset_data["ingredient_set-" + str(i) + "-amount"] = 1
        formset_data["ingredient_set-" + str(i) + "-id"] = i + 1
    return formset_data
