from django.shortcuts import render, redirect
from ..models import SocialMedia

def edit_social_media(request):
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
        return redirect('student_detail')
    
    context = {
        'social_media': social_media
    }
    if social_media:
        return render(request, 'social_link/edit_social_media.html', context)
    else:
       return render(request, 'msg/data_doesnot_create.html')
