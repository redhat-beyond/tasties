from django.db import models


class DummyModel(models.Model):
    test_field = models.CharField(max_length=16)
