from django.shortcuts import render, redirect


def pre_home(request):
    return render(request, 'pre_home/index.html')


def contactus(request):
    return render(request, 'pre_home/contactus.html')


def services(request):
    return render(request, 'pre_home/services.html')


def about(request):
    return render(request, 'pre_home/about.html')
