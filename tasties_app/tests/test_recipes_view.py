import pytest
from authConstants import VALID_USER, VALID_PASSWORD
from tasties_app.models import Comment
from django.core.exceptions import ObjectDoesNotExist


@pytest.mark.django_db
class TestRecipesView:
    def test_recipes_view(self, client, signed_up_credentials):
        response = client.get('/')
        assert response.status_code == 302
        assert response.url == '/login/?next=/'
        response = client.post('/login/', data={'username': VALID_USER, 'password': VALID_PASSWORD})
        assert response.status_code == 302
        assert response.url == '/'

    def test_view_recipe(self, client, signed_up_credentials, recipes):
        client.post('/login/', data={'username': VALID_USER, 'password': VALID_PASSWORD})
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

    def test_view_recipe_invalid_id(self, client, signed_up_credentials):
        client.post('/login/', data={'username': VALID_USER, 'password': VALID_PASSWORD})
        response = client.get('/view_recipe/test1/')
        assert response.status_code == 404

    def test_view_recipe_not_found(self, client, signed_up_credentials):
        client.post('/login/', data={'username': VALID_USER, 'password': VALID_PASSWORD})
        response = client.get('/view_recipe/99999999999/')
        assert response.status_code == 302
        assert response.url == '/'

    def test_add_comment_function(self, client, comment, recipe_test, create_user):
        client.force_login(create_user)
        response = client.get(f'/view_recipe/{recipe_test.id}/?comment-adding={comment.comment_text}')
        assert response.status_code == 200
        comment_test = Comment.objects.get(author_id=comment.author_id, comment_text=comment.comment_text)
        assert comment_test.comment_text == comment.comment_text

    def test_add_comment_function_invalid(self, client, create_user, recipe_test, comment):
        client.force_login(create_user)
        response = client.get(f'/view_recipe/{recipe_test.id}/?comment-adding={""}')
        assert response.status_code == 200
        with pytest.raises(ObjectDoesNotExist):
            Comment.objects.get(author_id=comment.author_id, comment_text="")
