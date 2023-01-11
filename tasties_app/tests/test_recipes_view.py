import pytest
from authConstants import VALID_USER, VALID_PASSWORD


@pytest.mark.django_db
class TestRecipesView:
    def test_recipes_view(self, client, signed_up_credentials):
        response = client.get('/')
        assert response.status_code == 302
        assert response.url == '/login/?next=/'
        response = client.post('/login/', data={'username': VALID_USER, 'password': VALID_PASSWORD})
        assert response.status_code == 302
        assert response.url == '/'

    def test_view_recipe(self, client, signed_up_credentials):
        client.post('/login/', data={'username': VALID_USER, 'password': VALID_PASSWORD})
        response = client.get('/view_recipe/')
        assert response.status_code == 302
        assert response.request['PATH_INFO'] == '/view_recipe/'

    def test_view_recipe_unauthorized(self, client):
        response = client.get('/view_recipe/')
        assert response.status_code == 302
        assert response.url == '/login/?next=/view_recipe/'
