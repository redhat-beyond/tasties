from django.shortcuts import render


def index(request):
    return render(request, 'tasties_app/index.html',)


def base(request):
    return render(request, 'tasties_app/base.html',)
