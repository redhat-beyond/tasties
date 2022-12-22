import pytest
from django.contrib.auth.models import User
from tasties_app.models import Category, Recipe
from django.db import IntegrityError
from django.core.exceptions import ValidationError


@pytest.fixture()
def recipes():
    """
    This fixture generates some test Recipes

    Returns:
        tuple<Recipe>: A number of Recipe test objects
    """
    user = User.objects.create_user("testuser1", "password")  # This is required to create Recipes
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
    category_1 = Category.objects.create(category_name="Breakfast")
    category_2 = Category.objects.create(category_name="Mushrooms")
    category_3 = Category.objects.create(category_name="Beef")
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


class TestCategoryModel:
    @pytest.mark.django_db
    def test_create_categories(self, categories, recipes):
        """
        Verifies fixtures 'categories' and 'recipes' properly
           saved their data as expected

        Args:
            categories (fixture): fixture 'categories'
            recipes (fixture): fixture 'recipes'
        """
        all_categories = Category.objects.all()
        all_recipes = Recipe.objects.all()
        for category in categories:
            assert category in all_categories
        for recipe in recipes:
            assert recipe in all_recipes

    @pytest.mark.django_db
    def test_get_recipes_by_category(self, categorized_recipes):
        """
        Verifies method 'get_recipes_by_category' provides intended functionality

        Args:
            categories (fixture): fixture 'categories'
            recipes (fixture): fixture 'recipes'
            categorized_recipes (fixture): fixture 'categorized_recipes'
        """
        # define test variables
        recipes = categorized_recipes[0]
        categories = categorized_recipes[1]

        category_1 = categories[0]
        category_2 = categories[1]
        category_3 = categories[2]
        recipe_1 = recipes[0]
        recipe_2 = recipes[1]
        # generate recipe_by_category QuerySets
        recipes_by_category_1 = Category.get_recipes_by_category(category_1)
        recipes_by_category_2 = Category.get_recipes_by_category(category_2)
        recipes_by_category_3 = Category.get_recipes_by_category(category_3)
        # assert expected results
        assert len(recipes_by_category_3) == 0  # category with no associated recipes will return empty set
        assert recipe_2 not in recipes_by_category_1
        assert recipe_1, recipe_2 in recipes_by_category_2
        assert len(Category.get_recipes_by_category("Cheese")) == 0  # invalid parameters will result in empty set

    @pytest.mark.django_db
    def test_category_name_uniqueness(self, categories):
        """
        Verifies that a new Category cannot be saved, if it has the same name as an existing Category

        Args:
            categories (fixture): test data generated by fixture 'categories'
        """
        category_4 = Category(category_name="Breakfast")
        with pytest.raises(IntegrityError):
            category_4.save()  # attempting to save a new category with the same name as an existing one

    @pytest.mark.django_db
    def test_category_name_length_limit(self):
        """
        Verifies that a name of invalid length cannot be given to a Category
        """
        category_too_long = Category(category_name="String longer than 16 characters")
        with pytest.raises(ValidationError):
            category_too_long.clean_fields()  # attempting to validate a category with a name that's too long
        category_too_short = Category("")
        with pytest.raises(ValidationError):
            category_too_short.clean_fields()  # attempting to validate a category with an empty string

    @pytest.mark.django_db
    def test_category_must_have_name(self):
        """
        Verifies that validators do not allow constructing a Category without non-empty 'category_name' field
        """
        with pytest.raises(ValidationError):
            category_no_argument = Category()
            category_no_argument.clean_fields()

    @pytest.mark.django_db
    def test_category_to_string(self, categories):
        """
        Verifies that __str__ method acts as expected

        Args:
            categories (fixture): fixture 'categories'
        """
        assert str(categories[0]) == "Breakfast"