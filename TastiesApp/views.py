from django.shortcuts import render


def index(request):
    return render(request, 'TastiesApp/index.html',)
# Create your views here.
