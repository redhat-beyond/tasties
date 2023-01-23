import pytest
from pytest_django.asserts import assertTemplateUsed
from authConstants import VALID_USER, VALID_PASSWORD


@pytest.mark.django_db
class TestRecipesView:
    def test_search(self, client, search_recipe):
        client.force_login(search_recipe.author_id)
        response = client.post('/search/', data={'search': 'salad'})
        assert search_recipe in response.context['recipes_list']
        assertTemplateUsed(response, 'tasties_app/recipes.html')

    def test_not_exsit_search(self, client, signed_up_credentials):
        client.post('/login/', data={'username': VALID_USER, 'password': VALID_PASSWORD})
        response = client.post('/search/', data={'search': 'abcdefg'})
        assert len(response.context['recipes_list']) == 0
