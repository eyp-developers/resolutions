from django.shortcuts import render


def home(request):
    return render(request, 'res/home.html')


def session(request):
    return render(request, 'res/session.html')


def committee(request):
    return render(request, 'res/committee.html')
