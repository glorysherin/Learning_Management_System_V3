from django.shortcuts import render, redirect, get_object_or_404
from base.models import YouTubeLink, Category
from .Tool.Tools import student_detials, staff_detials, get_user_role


def add_youtube_link(request,class_id):
    categories = Category.objects.filter(class_id = class_id)
    return render(request, 'youtube_links/add_youtube_link.html',staff_detials(request,'upload link',{'categories': categories,'class_id':class_id}) )

def save_youtube_link(request,class_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        link = request.POST.get('link')
        category_id = request.POST.get('category')
        new_category = request.POST.get('new_category')
        
        if category_id == 'new' and new_category:
            category = Category.objects.create(name=new_category,class_id=class_id)
        else:
            category = get_object_or_404(Category, pk=category_id)
        
        YouTubeLink.objects.create(title=title, link=link, category=category,class_id=class_id)
        
        return redirect('list_youtube_links', args=[class_id])

def list_youtube_links(request,class_id):
    links = YouTubeLink.objects.filter(class_id=class_id)
    if get_user_role(request) == "Student":
        return render(request, 'youtube_links/st_list_youtube_links.html',student_detials(request,'list link', {'links': links,'class_id':class_id}))
    elif get_user_role(request) == "staff":
        return render(request, 'youtube_links/list_youtube_links.html',staff_detials(request,'list link', {'links': links,'class_id':class_id}))


def edit_youtube_link(request, pk,class_id):
    link = get_object_or_404(YouTubeLink, pk=pk)
    categories = Category.objects.filter(class_id=class_id)
    
    if request.method == 'POST':
        link.title = request.POST.get('title')
        link.link = request.POST.get('link')
        category_id = request.POST.get('category')
        new_category = request.POST.get('new_category')
        
        if category_id == 'new' and new_category:
            category = Category.objects.create(name=new_category)
        else:
            category = get_object_or_404(Category, pk=category_id)
        
        link.category = category
        link.save()
        
        return redirect('list_youtube_links', class_id=class_id)
    
    return render(request, 'youtube_links/edit_youtube_link.html',staff_detials(request,'edit link', {'class_id':class_id,'link': link, 'categories': categories}))

def delete_youtube_link(request, pk,class_id):
    link = get_object_or_404(YouTubeLink, pk=pk)
    
    if request.method == 'POST':
        link.delete()
        return redirect('list_youtube_links', class_id=class_id)
    
    return render(request, 'youtube_links/delete_youtube_link.html',staff_detials(request,'delete link', {'link': link, 'class_id':class_id}))
