import pytest
from tasties_app.models import Recipe, Category
from django.utils import timezone
from django.contrib.auth.models import User


@pytest.fixture
def generate_data():
    """This fixture create the data we need for tests
    and save it in the data base. """

    user1 = User.objects.create_user(username='john', password='password')

    test_data = ['Test Recipe1', user1, 'Test Description1', 'Test Directions1', 1, 'test_picture1']

    category1 = Category.objects.create(category_name="1")
    recipe1 = Recipe(title=test_data[0], author_id=test_data[1], description=test_data[2], directions=test_data[3],
                     publication_date=timezone.now(), minutes_to_make=test_data[4], recipe_picture=test_data[5])

    category1.save()
    recipe1.save()
    recipe1.categories.add(category1)
    recipe1.save()
    category1.save()


class TestRecipeModel:

    @pytest.mark.django_db
    def test_save_recipe(self, generate_data):
        recipe_set = Recipe.objects.all()
        recipe1 = recipe_set[0]
        category1 = Category.objects.first()
        assert recipe1.title == "Test Recipe1"
        assert recipe1.author_id.username == "john"
        assert category1.category_name == "1"
        assert recipe1.description == "Test Description1"
        assert recipe1.directions == "Test Directions1"
        assert recipe1.minutes_to_make == 1
        assert recipe1.recipe_picture == "test_picture1"

    @pytest.mark.django_db
    def test_edit_recipe(self, generate_data):
        recipe_set = Recipe.objects.all()
        recipe1 = recipe_set[0]
        recipe1.edit_recipe("Test Recipe2", "Test Description2", "Test Directions2", 5, "test_picture2")
        assert recipe1.title == "Test Recipe2"
        assert recipe1.description == "Test Description2"
        assert recipe1.directions == "Test Directions2"
        assert recipe1.minutes_to_make == 5
        assert recipe1.recipe_picture == "test_picture2"

    @pytest.mark.django_db
    def test_delete_recipe(self, generate_data):
        recipe_set = Recipe.objects.all()
        recipe1 = recipe_set[0]
        recipe1.delete_recipe()
        assert len(recipe_set) == 0
