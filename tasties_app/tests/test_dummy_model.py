import pytest
from tasties_app.models import DummyModel


class TestDummyModel():

    @pytest.mark.django_db
    def test_fail_dummy_model_creation(self):
        dm = DummyModel(test_field="test field")
        assert dm not in DummyModel.objects.all()

    @pytest.mark.django_db
    def test_pass_dummy_model_creation(self):
        dm = DummyModel(test_field="test field")
        dm.save()
        assert dm in DummyModel.objects.all()
    # makemigrations LOCALLY, but DO NOT commit 0001_initial.py
