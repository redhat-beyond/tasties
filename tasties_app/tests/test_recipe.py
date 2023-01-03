import pytest
from tasties_app.models import Recipe
from django.core.exceptions import ValidationError, ObjectDoesNotExist


class TestRecipeModel:
    """
        This class test the recipe model and the method.
    """

    @pytest.mark.django_db
    def test_save_recipe(self, recipe):
        assert recipe in Recipe.objects.all()

    @pytest.mark.django_db
    def test_recipe_fields(self, recipe):
        recipe1 = Recipe.objects.filter(author_id=recipe.author_id)[0]
        assert recipe1.title == "Test Recipe1"
        assert recipe1.author_id.username == "john"
        assert recipe1.description == "Test Description1"
        assert recipe1.directions == "Test Directions1"
        assert recipe1.minutes_to_make == 1
        assert recipe1.recipe_picture == "test_picture1"

    @pytest.mark.django_db
    def test_delete_recipe(self, recipe):
        recipe.delete()
        with pytest.raises(ObjectDoesNotExist):
            Recipe.objects.get(pk=recipe.id)

    @pytest.mark.django_db
    def test_str_function(self, recipe):
        assert recipe.__str__() == "Test Recipe1"

    @pytest.mark.django_db
    def test_invalid_title(self, recipe):
        recipe1 = Recipe.objects.filter(author_id=recipe.author_id)
        recipe1.update(title="")
        with pytest.raises(ValidationError):
            recipe1[0].full_clean()

    @pytest.mark.django_db
    def test_invalid_description(self, recipe):
        recipe1 = Recipe.objects.filter(author_id=recipe.author_id)
        recipe1.update(description="")
        with pytest.raises(ValidationError):
            recipe1[0].full_clean()

    @pytest.mark.django_db
    def test_invalid_directions(self, recipe):
        recipe1 = Recipe.objects.filter(author_id=recipe.author_id)
        recipe1.update(directions="")
        with pytest.raises(ValidationError):
            recipe1[0].full_clean()

    @pytest.mark.django_db
    def test_invalid_minutes_to_make(self, recipe):
        recipe1 = Recipe.objects.filter(author_id=recipe.author_id)
        recipe1.update(minutes_to_make=0)
        with pytest.raises(ValidationError):
            recipe1[0].full_clean()
