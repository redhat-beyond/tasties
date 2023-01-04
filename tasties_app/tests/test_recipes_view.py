import pytest
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
class TestRecipesView:
    def test_recipes_view(self, client):
        response = client.get('/recipes/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'tasties_app/recipes.html')
