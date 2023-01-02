from django.shortcuts import render
from tasties_app.models import Category


def index(request):
    return render(request, 'tasties_app/index.html',)


def base(request):
    objects = Category.objects.all()
    return render(request, 'tasties_app/base.html', {'objects': objects})
