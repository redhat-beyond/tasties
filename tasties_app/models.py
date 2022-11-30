from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MinLengthValidator, MaxValueValidator


class Category(models.Model):
    category_name = models.CharField(max_length=16, unique=True)


class Recipe(models.Model):
    """

    This class represent Recipe object

    Fields:
        title (string) : Title of the recipe.
        author_id (User) : User object.
        categories (Categories) : Categories object.
        description (string) : Description of the recipe.
        directions (string) : Directions how to make the recipe.
        publication_date (DateTime) : When was the recipe published.
        minutes_to_make (int) : How long does it take to make the recipe.
        recipe_picture (Image) : A picture that describes the recipe.

    """
    title = models.CharField(max_length=64, validators=[MinLengthValidator(1)], unique=True)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    description = models.CharField(max_length=512, validators=[MinLengthValidator(1)])
    directions = models.CharField(max_length=65536, validators=[MinLengthValidator(1)])
    publication_date = models.DateTimeField(auto_now_add=timezone.now())
    minutes_to_make = models.IntegerField(validators=[MinValueValidator(1)])
    recipe_picture = models.ImageField(upload_to='recipe_pictures')

    def edit_recipe(self, new_title, new_description,
                    new_directions, new_minutes_to_make,
                    new_recipe_pic):
        """
        This function designed to allow the user to edit his recipe.

        Fields:
            new_title (string) : The new given title to the recipe.
            new_description (string) : The new or edited recipe description
                                        given to the recipe.
            new_directions (string) : The new or edited directions given to the recipe.
            new_minutes_to_make (int) : The updating the preparation time of the recipe.
            new_recipe_pic (Image) : The new picture that describes the recipe.
        """
        self.title = new_title
        self.description = new_description
        self.directions = new_directions
        self.minutes_to_make = new_minutes_to_make
        self.recipe_picture = new_recipe_pic
        self.save()


class Ingredient(models.Model):

    class UnitChoices(models.TextChoices):

        WHOLE = "Whole"
        FLOZ = "Fluid Ounce"
        TSP = "Tea Spoon"
        OZ = "Ounce"
        CUP = "Cup"
        GRAM = "Gram"
        ML = "Milliliter"

    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0001)])
    measurement_unit = models.CharField(max_length=11, choices=UnitChoices.choices, default=UnitChoices.WHOLE)
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
