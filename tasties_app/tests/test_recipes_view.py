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

    def test_view_recipe(self, client, signed_up_credentials, recipes, login_to_site):
        recipe = recipes[0]
        response = client.get(f'/view_recipe/{recipe.id}/')
        assert response.status_code == 200
        assert response.request['PATH_INFO'] == f'/view_recipe/{recipe.id}/'
        assert response.context['recipe'] == recipe

    def test_view_recipe_unauthorized(self, client, recipes):
        recipe = recipes[0]
        response = client.get(f'/view_recipe/{recipe.id}/')
        assert response.status_code == 302
        assert response.url == f'/login/?next=/view_recipe/{recipe.id}/'

    def test_view_recipe_invalid_id(self, client, signed_up_credentials, login_to_site):
        response = client.get('/view_recipe/test1/')
        assert response.status_code == 404

    def test_view_recipe_not_found(self, client, signed_up_credentials, login_to_site):
        response = client.get('/view_recipe/99999999999/')
        assert response.status_code == 302
        assert response.url == '/'

    def test_sort_by_name(self, client, signed_up_credentials, recipe):
        recipe.title = 'AAA Test'
        recipe.save()
        client.post('/login/', data={'username': VALID_USER, 'password': VALID_PASSWORD})
        response = client.post('/', data={'action': 'Sort', 'sort_by': 'name'})
        assert response.status_code == 200
        assert response.context['recipes_list'][0] == recipe

    def test_sort_by_date(self, client, signed_up_credentials, recipe):
        recipe.publication_date = '2030-01-01'
        recipe.save()
        client.post('/login/', data={'username': VALID_USER, 'password': VALID_PASSWORD})
        response = client.post('/', data={'action': 'Sort', 'sort_by': 'date'})
        assert response.status_code == 200
        assert response.context['recipes_list'][0] == recipe


@pytest.mark.django_db
class TestFilteringRecipes:
    def test_category_view(self, client, signed_up_credentials, categorized_recipes):
        client.post(
            "/login/", data={"username": VALID_USER, "password": VALID_PASSWORD}
        )
        category = categorized_recipes[1][0]
        recipe = categorized_recipes[0][0]
        response = client.post(f"/?category={category}")
        assert response.status_code == 200
        assert len(response.context["recipes_list"]) == 1
        assert recipe in response.context["recipes_list"]

    def test_remove_filter(self, client, signed_up_credentials, categorized_recipes):
        client.post("/login/", data={"username": VALID_USER, "password": VALID_PASSWORD})
        categories = [
            categorized_recipes[1][0],
            categorized_recipes[1][1],
            categorized_recipes[1][2],
        ]
        response = client.post("/")
        assert response.status_code == 200
        for category in categories:
            assert category in categories
