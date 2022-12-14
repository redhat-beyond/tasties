from enum import Enum

from django.contrib.auth.models import User
from django.core.validators import (
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.db import models
from django.utils import timezone


class Category(models.Model):
    category_name = models.CharField(max_length=16, unique=True)


class Recipe(models.Model):
    title = models.CharField(
        max_length=64, validators=[MinLengthValidator(1)], unique=True
    )
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    description = models.CharField(max_length=512, validators=[MinLengthValidator(1)])
    directions = models.CharField(max_length=65536, validators=[MinLengthValidator(1)])
    publication_date = models.DateField(default=timezone.now)
    minutes_to_make = models.IntegerField(validators=[MinValueValidator(1)])
    recipe_picture = models.ImageField(upload_to="recipe_pictures")


class Ingredient(models.Model):
    """
    Ingredient Model - represents an ingredient in a recipe.
    Fields:
        UNIT_CHOICES - a list of valid measurement units
        recipe_id - the recipe that the ingredient belongs to
        amount - the amount of the ingredient
        measurement_unit - the unit of measurement for the ingredient
        description - a description of the ingredient
    """
    class UnitChoices(models.TextChoices, Enum):
        WHOLE = "Whole"
        FLOZ = "Fluid Ounce"
        TSP = "Tea Spoon"
        OZ = "Ounce"
        CUP = "Cup"
        GRAM = "Gram"
        ML = "Milliliter"

    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0001)]
    )
    measurement_unit = models.CharField(
        max_length=11, choices=UnitChoices.choices, default=UnitChoices.WHOLE
    )
    description = models.CharField(max_length=64, validators=[MinLengthValidator(1)])

    def __str__(self):
        return str(self.amount) + " " + self.measurement_unit + " " + self.description


class Comment(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    publication_date = models.DateField(default=timezone.now)
    comment_text = models.CharField(max_length=512, validators=[MinLengthValidator(1)])


class Rating(models.Model):
    """
    This Class represent Rating object

    Fields:
        author_id (User): User object.
        recipe_id (Recipe): Recipe object.
        rating (int): rating for the recipe, 1-5
    """

    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def update_rating(self, new_rate):
        """
        This function update the rating for given recipe

        Args:
            new_rate(int): the new rating for the recipe
        """
        if type(new_rate) != int or new_rate > 5 or new_rate < 1:
            raise ValueError("Invalid value")
        self.rating = new_rate
