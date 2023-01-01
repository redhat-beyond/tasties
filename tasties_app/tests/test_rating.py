import pytest
from tasties_app.models import Rating


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
