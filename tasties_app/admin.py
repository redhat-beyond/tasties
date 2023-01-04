from django.contrib import admin

# Register your models here.
from .models import Category, Comment, Rating, Recipe, Ingredient

admin.site.register(Rating)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Recipe)
admin.site.register(Ingredient)
