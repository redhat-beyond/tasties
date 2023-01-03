import pytest
from tasties_app.models import Rating
from django.core.exceptions import ObjectDoesNotExist


class TestRatingModel:
    @pytest.mark.django_db
    def test_add_rating(self, rating):
        assert rating in Rating.objects.all()

    @pytest.mark.django_db
    def test_delete_rating(self, rating):
        rating.delete()
        with pytest.raises(ObjectDoesNotExist):
            Rating.objects.get(pk=rating.id)

    @pytest.mark.django_db
    def test_edit_rating(self, rating):
        rating_to_update = Rating.objects.get(pk=rating.id)
        assert rating_to_update.rating == 3
        rating_to_update.update_rating(4)
        rating_to_update.save()
        assert Rating.objects.get(pk=rating.id).rating == 4

    @pytest.mark.django_db
    def test_add_bad_rating(self, rating):
        """
        Checking that we can't add rating with
        number that is more than 5 or less than 1

        Args:
            rating = rating object
        """
        with pytest.raises(ValueError):
            rating.update_rating(6)
        with pytest.raises(ValueError):
            rating.update_rating(0)

    @pytest.mark.django_db
    def test_invalid_rating_author_id(self, rating):
        """
        Checking that we can't add rating with author_id of type other than User

        Args:
            rating = rating object
        """
        with pytest.raises(ValueError):
            rating.author_id = 5
