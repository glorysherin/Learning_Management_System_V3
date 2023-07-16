from django.shortcuts import render, redirect, get_object_or_404
from base.models import YouTubeLink, Category, Teacher
from .Tool.Tools import student_detials, staff_detials, get_user_role
from django.contrib.auth.models import User


def add_youtube_link(request,class_id):
    categories = Category.objects.filter(class_id = class_id)
    return render(request, 'youtube_links/add_youtube_link.html',staff_detials(request,'upload link',{'categories': categories,'class_id':class_id}) )

def save_youtube_link(request,class_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        iframe_link = request.POST.get('link')
        category_id = request.POST.get('category')
        new_category = request.POST.get('new_category')
        
        if category_id == 'new' and new_category:
            category = Category.objects.create(name=new_category,class_id=class_id)
        else:
            category = get_object_or_404(Category, pk=category_id)
            
        new_width = 300
        new_height = 250

        # Extract the width and height attributes from the iframe link
        width_start = iframe_link.find('width="') + 7
        width_end = iframe_link.find('"', width_start)
        height_start = iframe_link.find('height="') + 8
        height_end = iframe_link.find('"', height_start)

        # Replace the width and height values with the new values
        modified_iframe_link = (
            iframe_link[:width_start] +
            str(new_width) +
            iframe_link[width_end:height_start] +
            str(new_height) +
            iframe_link[height_end:]
        )
        
        YouTubeLink.objects.create(title=title, link=modified_iframe_link, category=category,class_id=class_id)
        
        return redirect('list_youtube_links', class_id=class_id)

def list_youtube_links(request,class_id):
    links = YouTubeLink.objects.filter(class_id=class_id)
    Category = []
    for i in links:
        Category.append(i.category)
    print(get_user_role(request))
    try:
        Teacher.objects.get(user=User.objects.get(id=request.user.id))
        return render(request, 'youtube_links/list_youtube_links.html',staff_detials(request,'list link', {'links': links,'class_id':class_id,'categories':list(set(Category))}))
    except:
        return render(request, 'youtube_links/st_list_youtube_links.html',student_detials(request,'list link', {'links': links,'class_id':class_id,'categories':list(set(Category))}))

def std_list_youtube_links(request,class_id):
    links = YouTubeLink.objects.filter(class_id=class_id)
    Category = []
    for i in links:
        Category.append(i.category)
    print(Category)
    return render(request, 'youtube_links/st_list_youtube_links.html',student_detials(request,'list link', {'links': links,'class_id':class_id,'categories':list(set(Category))}))


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

def list_notes(request,class_id):
    return render(request,'youtube_links/list_notes.html',student_detials(request,"List notes",{'class_id':class_id}))

