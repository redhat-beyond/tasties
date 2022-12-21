import pytest
from tasties_app.models import Recipe, Category
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


@pytest.fixture
def recipe():
    """
        This fixture create the data we need for tests
        and save it in the data base.
    """
    user1 = User.objects.create_user(username='john', password='password')
    test_data = ['Test Recipe1', user1, 'Test Description1', 'Test Directions1', 1, 'test_picture1']
    category1 = Category.objects.create(category_name="1")
    recipe1 = Recipe(title=test_data[0], author_id=test_data[1], description=test_data[2], directions=test_data[3],
                     publication_date=timezone.now(), minutes_to_make=test_data[4], recipe_picture=test_data[5])
    recipe1.full_clean()
    category1.full_clean()
    category1.save()
    recipe1.save()
    recipe1.categories.add(category1)
    recipe1.save()
    return recipe1


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
        assert len(Recipe.objects.all()) == 0

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
