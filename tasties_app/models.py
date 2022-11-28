from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MinLengthValidator, MaxValueValidator


class Category(models.Model):
    category_name = models.CharField(max_length=16, unique=True)


class Recipe(models.Model):
    title = models.CharField(max_length=64, validators=[MinLengthValidator(1)], unique=True)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    description = models.CharField(max_length=512, validators=[MinLengthValidator(1)])
    directions = models.CharField(max_length=65536, validators=[MinLengthValidator(1)])
    publication_date = models.DateField(default=timezone.now)
    minutes_to_make = models.IntegerField(validators=[MinValueValidator(1)])
    recipe_picture = models.ImageField(upload_to='recipe_pictures')


class Ingredient(models.Model):
    WHOLE = "WHOLE"
    FLOZ = "FLOZ"
    TSP = "TSP"
    OZ = "OZ"
    CUP = "CUP"
    GRAM = "GRAM"
    ML = "ML"
    UNIT_CHOICES = ((WHOLE, 'Whole'),
                    (FLOZ, 'Fluid Ounce'),
                    (TSP, 'Teaspoon'),
                    (OZ, 'Ounce'),
                    (CUP, 'Cup'),
                    (GRAM, 'Gram'),
                    (ML, 'Milliliter'),
                    )

    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0001)])
    measurement_unit = models.CharField(max_length=8, choices=UNIT_CHOICES, default=WHOLE)
    description = models.CharField(max_length=64, validators=[MinLengthValidator(1)])


class Comment(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    publication_date = models.DateField(default=timezone.now)
    comment_text = models.CharField(max_length=512, validators=[MinLengthValidator(1)])


class Rating(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
