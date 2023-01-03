from django.shortcuts import render
from tasties_app.models import Category


def index(request):
    return render(request, 'tasties_app/index.html',)


def base(request):
    categories_list = Category.objects.all()
    return render(request, 'tasties_app/base.html', {'objects': categories_list})
