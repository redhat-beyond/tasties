import pytest as pytest

from tasties_app.models import Ingredient, Recipe, Category
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


@pytest.fixture
def ingredient():
    """
    Creates a user, a recipes, and an ingredient,
    and adds them to the database.
    returns: ingredient
    """
    user1 = User.objects.create_user('test_user', 'password')
    category = Category.objects.create(category_name='Breakfast')
    category.save()
    recipe = Recipe(title='Test Recipe1', author_id=user1, description='Test Description1',
                    directions='Test Directions1', minutes_to_make=1, recipe_picture='test_picture1')
    recipe.save()
    recipe.categories.add(category)
    ingredient = Ingredient(recipe_id=recipe, amount=1.0, measurement_unit='WHOLE',
                            description='test ingredient')
    ingredient.save()
    return ingredient


class TestIngredientModel:
    """
    Tests the Ingredient model:
        - Creation of an ingredient
        - Editing of an ingredient
        - Negative tests to ensure that invalid data cannot be added to the database
    """
    @pytest.mark.django_db
    def test_ingredient_fixture(self, ingredient):
        assert ingredient in Ingredient.objects.all()

    @pytest.mark.django_db
    def test_edit_ingredient(self, ingredient):
        ingredient.amount = 2.0
        ingredient.measurement_unit = "Fluid Ounce"
        ingredient.description = "test2"
        ingredient.full_clean()
        ingredient.save()
        ingredient_to_check = Ingredient.objects.get(id=ingredient.id)
        assert ingredient_to_check.amount == 2.0
        assert ingredient_to_check.measurement_unit == "Fluid Ounce"
        assert ingredient_to_check.description == "test2"

    @pytest.mark.django_db
    def test_invalid_amount_input(self, ingredient):
        with pytest.raises(ValidationError):
            recipe = Recipe.objects.all()[0]
            ingredient2 = Ingredient(recipe_id=recipe, amount=-3, measurement_unit="FLOZ", description="test2")
            ingredient2.full_clean()
            ingredient2.save()

    @pytest.mark.django_db
    def test_invalid_measurement_edit(self, ingredient):
        with pytest.raises(ValidationError):
            ingredient.measurement_unit = "FF"
            ingredient.full_clean()
            ingredient.save()

    @pytest.mark.django_db
    def test_add_ingredients(self, ingredient):
        recipe = Recipe.objects.all()[0]
        ingredient2 = Ingredient(recipe_id=recipe, amount=3, measurement_unit="Whole", description="test2")
        ingredient2.save()
        assert ingredient2 in Ingredient.objects.all()
