from django.shortcuts import render, redirect
from ..models import SocialMedia, Teacher
from django.contrib.auth.models import User

def edit_social_media(request,id):
    if request.user.id:
        try:
            try:
                social_media =  SocialMedia.objects.get(std_id=id)
            except:
                social_media =  SocialMedia.objects.get(std_id=request.user.id)
        except:
            social_media = SocialMedia.objects.create(std_id=request.user.id)
            
    if request.method == 'POST':
        social_media.portfolio = request.POST.get('portfolio')
        social_media.twitter = request.POST.get('twitter')
        social_media.linkedin = request.POST.get('linkedin')
        social_media.github = request.POST.get('github')
        social_media.facebook = request.POST.get('facebook')
        social_media.instagram = request.POST.get('instagram')
        social_media.save()

        return redirect('student_detail',student_id=id)
    
    context = {
        'social_media': social_media,
        'usr_id':id
    }
    if social_media:
        return render(request, 'social_link/edit_social_media.html', context)
    else:
       return render(request, 'msg/data_doesnot_create.html')

def staff_edit_social_media(request):
    if request.user.id:
        try:
            social_media =  SocialMedia.objects.get(std_id=request.user.id)
        except:
            social_media = SocialMedia.objects.create(std_id=request.user.id)
            
    if request.method == 'POST':
        social_media.portfolio = request.POST.get('portfolio')
        social_media.twitter = request.POST.get('twitter')
        social_media.linkedin = request.POST.get('linkedin')
        social_media.github = request.POST.get('github')
        social_media.facebook = request.POST.get('facebook')
        social_media.instagram = request.POST.get('instagram')
        social_media.save()
        usr = User.objects.get(id=request.user.id)
        staff_id = Teacher.objects.get(user=usr)
        return redirect('teacher_profile', staff_id=staff_id.id )
    
    context = {
        'social_media': social_media
    }
    if social_media:
        return render(request, 'social_link/staff_edit_social_media.html', context)
    else:
       return render(request, 'msg/data_doesnot_create.html')


def class_blank(request):
    return render(request,'msg/class_blank.html')