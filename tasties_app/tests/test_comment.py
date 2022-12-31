import pytest
from tasties_app.models import Comment
from django.core.validators import ValidationError


class TestComment():

    @pytest.mark.django_db
    def test_add_comment(self, comment):
        comment_object2 = Comment(author_id=comment.author_id, recipe_id=comment.recipe_id,
                                  comment_text='test comment2')
        comment_object2.save()
        assert comment_object2 in Comment.objects.all()

    @pytest.mark.django_db
    def test_empty_comment(self, comment):
        with pytest.raises(ValidationError):
            comment_object2 = Comment(author_id=comment.author_id, recipe_id=comment.recipe_id,
                                      comment_text='')
            comment_object2.full_clean()
            comment_object2.save()
            assert comment_object2 in Comment.objects.all()
