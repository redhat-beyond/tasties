import pytest
from authConstants import VALID_USER, VALID_PASSWORD
from tasties_app.models import Recipe
from django.core.exceptions import ObjectDoesNotExist
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db
class TestEditRecipe:
    def test_require_login(self, client, recipe_test, signed_up_credentials):
        """
        This test verifies that a user must be logged
        in to edit a recipe. If a user is not logged in,
        redirect to '/' is expected.

        Args:
            client : Django testing client
            signed_up_credentials (fixture): creates a user
        """
        response = client.get("/edit_recipe/"+str(recipe_test.id)+"/")
        assert response.status_code == 302
        assert (
            response.url == "/login/?next=/edit_recipe/"+str(recipe_test.id)+"/"
        )
        response = client.post(
            "/login/", data={"username": VALID_USER, "password": VALID_PASSWORD}
        )
        assert response.status_code == 302
        assert response.url == "/"

    def test_unauthorized_access(self, client, recipe_test, signed_up_credentials, login_to_site):
        """
        This test verifies that a logged in user cannot edit a recipe authored
        by a different user

        Args:
            client : Django testing client
            recipe_test (fixture): creates a user, and a recipe owned by it
            signed_up_credentials (fixture): creates a user
            login_to_site (fixture): logs in user created by signed_up_credentials
        """
        response = client.get("/edit_recipe/"+str(recipe_test.id)+"/")
        assert response.status_code == 302
        assert (
            response.url == "/"
        )

    def test_valid_edits(
        self,
        client,
        recipe_test,
        form_data,
        formset_data
    ):
        """
        This test verifies that valid edits to a recipe
        using the view function edit_recipe will be saved

        Args:
            client : Django testing client
            recipe_test (fixture): creates a user, and a recipe owned by it
            form_data (dictionary): raw data for recipe form
            formset_data (dictionary): raw data for ingredient formset
        """
        author = recipe_test.author_id
        recipe_id = recipe_test.id
        client.force_login(author)
        response = client.get("/edit_recipe/"+str(recipe_id)+"/")
        assertTemplateUsed(response, 'tasties_app/edit_recipe.html')  # assert on edit page

        form_data.update(formset_data)
        response = client.post(
            "/edit_recipe/"+str(recipe_id)+"/", data=form_data
        )

        assert Recipe.objects.filter(title=form_data['title']).exists()
        saved_recipe = Recipe.objects.get(title=form_data['title'])
        assert saved_recipe.author_id == author
        assert saved_recipe.id == recipe_id
        assert response.status_code == 302
        assert response.url == "/view_recipe/" + str(saved_recipe.id) + "/"

    def test_no_ingredients(
        self, client, recipe_test, form_data
    ):
        """
        This tests verifies that a recipe without ingredients
        cannot be saved.

        Args:
            client : Django testing client
            signed_up_credentials (fixture): creates a user
            login_to_site (fixture): logs in user created by signed_up_credentials
            form_data (dictionary): raw data for recipe form
        """
        author = recipe_test.author_id
        recipe_id = recipe_test.id
        client.force_login(author)
        response = client.get("/edit_recipe/"+str(recipe_id)+"/")
        assertTemplateUsed(response, 'tasties_app/edit_recipe.html')

        response = client.post(
            "/edit_recipe/"+str(recipe_id)+"/", data=form_data
        )
        with pytest.raises(ObjectDoesNotExist):
            Recipe.objects.get(title=form_data['title'])
        assertTemplateUsed(response, 'tasties_app/create_recipe.html')
