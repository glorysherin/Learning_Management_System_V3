from django.shortcuts import render
from .Tool.blogTool import get_images


def pre_home(request):
    item = get_images()
    return render(request, 'pre_home/index.html', {"categories": item[0], "images": item[1]})


def contactus(request):
    return render(request, 'pre_home/contactus.html')


def services(request):
    return render(request, 'pre_home/services.html')


def about(request):
    return render(request, 'pre_home/about.html')
