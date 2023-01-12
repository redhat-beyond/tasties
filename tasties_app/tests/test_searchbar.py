import pytest
from pytest_django.asserts import assertTemplateUsed
from authConstants import VALID_USER, VALID_PASSWORD


@pytest.mark.django_db
class TestRecipesView:
    def test_search(self, client, recipes_filtered_by_salad, signed_up_credentials):
        client.post('/login/', data={'username': VALID_USER, 'password': VALID_PASSWORD})
        response = client.post('', data={'search': 'salad'})
        assert recipes_filtered_by_salad in response.context['recipes_with_ratings']
        assertTemplateUsed(response, 'tasties_app/recipes.html')

    def test_empty_search(self, client, signed_up_credentials):
        client.post('/login/', data={'username': VALID_USER, 'password': VALID_PASSWORD})
        response = client.post('', data={'search': 'abcdefg'})
        assert len(response.context['recipes_with_ratings']) == 0
