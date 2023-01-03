from django.db import migrations, transaction, IntegrityError
from tasties_app.models import Category
from django.core.exceptions import ValidationError


class Migration(migrations.Migration):

    dependencies = [
        ('tasties_app', '0002_alter_category_category_name'),
    ]

    def generate_data(apps, schema_editor):
        categories = ['Breakfast', 'Lunch', 'Dinner', 'Dessert', 'Snack', 'Bakery',
                      'Soup', 'Salad', 'Appetizer', 'Sauce', 'Beverage', 'Smoothie', 'Cocktail',
                      'Italian', 'Mexican', 'Chinese', 'Indian', 'Thai', 'Japanese', 'Korean',
                      'Vietnamese', 'Mediterranean', 'Middle Eastern', 'African', 'Caribbean',
                      'South American', 'Central American', 'Vegan', 'Vegetarian', 'Paleo',
                      'Gluten-Free', 'Dairy-Free', 'Low-Carb', 'Meat', 'Seafood',
                      'Poultry', 'Beef', 'Lamb', 'Pork', 'Sushi', 'Ramen', 'Pho',
                      'Taco', 'Burrito', 'Enchilada', 'Quesadilla', 'Tamale']

        with transaction.atomic():
            for category in categories:
                try:
                    category_object = Category(category_name=category)
                    category_object.full_clean()
                    category_object.save()
                except IntegrityError:
                    continue
                except ValidationError:
                    continue

    operations = [
        migrations.RunPython(generate_data), ]
