import pytest
from tasties_app.models import Comment, Recipe
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date


@pytest.fixture
def generate_comments():
    """
    in this generate function we create User, Category and Recipe
    objects to fill Comment class and used to test
     """
    user = User.objects.create_user(username='test_user', password='password')
    recipe = Recipe(title='Test Recipe1', author_id=user, description='Test Description1',
                    directions='Test Directions1', publication_date=timezone.now(), minutes_to_make=1,
                    recipe_picture='recipe.jpeg')
    recipe.save()
    the_date = date.today().strftime("%Y-%m-%d")
    comment = Comment(author_id=user, recipe_id=recipe, publication_date=the_date, comment_text='test comment')
    comment.save()


class TestComment():
    @pytest.mark.django_db
    def test_str(self, generate_comments):
        user = User.objects.get(username='test_user')
        comment = Comment.objects.filter(author_id=user)
        the_date = str(date.today().strftime("%Y-%m-%d"))
        expected_comment1_str = user.get_username()+' '+comment[0].comment_text+' '+the_date
        assert expected_comment1_str == comment[0].__str__()

    @pytest.mark.django_db
    def test_add_comment(self, generate_comments):
        user = User.objects.get(username='test_user')
        filter_comment = Comment.objects.filter(author_id=user)
        comment_object = filter_comment[0]
        comment_object.add_comment('new comment')
        comment_object = filter_comment[1]
        if len(comment_object.comment_text) < 1:
            raise ("len the text is illegal")
        assert comment_object.comment_text == 'new comment'
