import pytest
from django.contrib.auth.models import User
from tasties_app.models import Rating, Recipe


@pytest.fixture()
def rating():
    """
    This fixture create the data we need in order to execute the tests.
    """
    user1 = User.objects.create_user("testuser1", "password")
    recipe = Recipe(
        title="Test Recipe1",
        author_id=user1,
        description="Test Description1",
        directions="Test Directions1",
        minutes_to_make=1,
        recipe_picture="test_picture2",
    )
    recipe.save()

    rating = Rating(author_id=user1, recipe_id=recipe, rating=3)
    rating.save()
    return rating


class TestRatingModel:
    @pytest.mark.django_db
    def test_add_rating(self, rating):
        assert rating in Rating.objects.all()

    @pytest.mark.django_db
    def test_delete_rating(self, rating):
        rating.delete()
        assert len(Rating.objects.all()) == 0

    @pytest.mark.django_db
    def test_edit_rating(self, rating):
        rating_set = Rating.objects.all()
        rating = rating_set[0]
        rating.update_rating(4)
        assert rating.rating == 4

    @pytest.mark.django_db
    def test_add_bad_rating(self, rating):
        """
        Checking that we can't add rating with
        number that is more than 5 or less than 1

        Args:
            rating = rating object
        """
        rating_set = Rating.objects.all()
        rating = rating_set[0]
        with pytest.raises(ValueError):
            rating.update_rating(6)
        with pytest.raises(ValueError):
            rating.update_rating(0)

    @pytest.mark.django_db
    def test_invalid_rating_author_id(self, rating):
        """
        Checking that we can't add rating with wrong author_id

        Args:
            rating = rating object
        """
        rating_set = Rating.objects.all()
        rating = rating_set[0]
        with pytest.raises(ValueError):
            rating.author_id = 5
