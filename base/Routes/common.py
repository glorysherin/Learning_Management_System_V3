import random
import time
import json

from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ..models import Faculty_details, Users, Room, Message, RoomMember, Gallery, Student, Department
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .Tool.blogTool import get_images
from .Tool.Tools import student_detials, staff_detials
from base import models as TMODEL
from base import models as SMODEL
from base import models
from .study import is_admin
from django.contrib.auth.decorators import login_required, user_passes_test


def student_home(request):
    usr_id = request.user.id
    usr_obj = User.objects.get(id=usr_id)
    std_data = Student.objects.get(user=usr_obj)
    usr = Users.objects.get(user_name=usr_obj.username)
    print(std_data)
    department = Department.objects.all()
    context = {
        'total_student': SMODEL.Student.objects.all().count(),
        'total_teacher': TMODEL.Teacher.objects.all().filter(status=True).count(),
        'total_course': models.Course.objects.all().count(),
        'user_name': usr_obj.username, 'detials': std_data, 'User': usr, 'std': std_data,
        'department':department
    }
    return render(request, "home/index.html", student_detials(request, 'Student home', context))


@login_required()
def staff_home(request):
    usr_id = request.user.id
    usr_obj = User.objects.get(id=usr_id)
    name = Users.objects.get(user_name=usr_obj.username)
    faculty_details = Faculty_details.objects.get(user_name=name.user_name)
    department = Department.objects.all()
    context = {
        'total_student': SMODEL.Student.objects.all().count(),
        'total_teacher': TMODEL.Teacher.objects.filter(status=True,role="staff").count(),
        'total_course': models.NoteCourse.objects.all().count(),
        'user_name': usr_obj.username, 'detials': faculty_details,
        'name_s': faculty_details.name.split(' '),
        'rolenum':name.role,
        'department':department
    }
    print(name.role)
    return render(request, "home/staff.html", staff_detials(request,'Home',context))


# Video Chat.....
def lobby(request):
    return render(request, 'base/lobby.html', student_detials(request, 'Conference'))


def staff_lobby(request):
    return render(request, 'base/staff_lobby.html', staff_detials(request, 'Conference'))


def admin_lobby(request):
    return render(request, 'base/admin_lobby.html')


def video_chat_room(request):
    return render(request, 'base/room.html')


def getToken(request):
    appId = "6c195af2970e48579689b47d0debf9ca"
    appCertificate = "acb5f43b05c74985aec64f691cf4311c"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(
        appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name': data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
    )
    name = member.name
    return JsonResponse({'name': member.name}, safe=False)


@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    member.delete()
    return JsonResponse('Member deleted', safe=False)


# ....... room chating


def chat_home(request):
    return render(request, 'chat_room/home.html', student_detials(request, 'Chat Home'))


def staff_chat_home(request):
    return render(request, 'chat_room/staff_home.html', staff_detials(request, 'Chat Home'))


def admin_chat_home(request):
    return render(request, 'chat_room/admin_home.html', staff_detials(request,'Chat Room'))


def admin_chat_room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'chat_room/admin_room.html', staff_detials(request,'Chat Room',{
        'page': 'Chat - '+str(room),
        'username': username,
        'room': room,
        'room_details': room_details,
    }))


def staff_chat_room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'chat_room/home_room.html', staff_detials(request, 'Chat - '+str(room), {

        'username': username,
        'room': room,
        'room_details': room_details,
    }))


def chat_room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'chat_room/room.html', student_detials(request, 'Chat - '+str(room), {

        'username': username,
        'room': room,
        'room_details': room_details,
    }))


def staff_chat_room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'chat_room/staff_room.html', staff_detials(request, 'Chat - '+str(room), {

        'username': username,
        'room': room,
        'room_details': room_details,
    }))


def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/chat'+'/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/chat'+'/'+room+'/?username='+username)


def staff_checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/staffchat'+'/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/staffchat'+'/'+room+'/?username='+username)


def admin_checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/adminchat'+'/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/adminchat'+'/'+room+'/?username='+username)


def Ncheckview(request):
    room = request.GET['room_name']
    username = request.GET['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/chat'+'/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/chat'+'/'+room+'/?username='+username)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    print(message, username, room_id)
    new_message = Message.objects.create(
        value=message, user=username, room=room_id)
    new_message.save()
    return JsonResponse({'msg':'sucess'})


def getMessages(request,  room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})


def chatgetMessages(request,  room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages": list(messages.values())})


# ...............gallery.......................................
def gallery(request):
    item = get_images()
    return render(request, "Gallery/gallery.html", {"categories": item[0], "images": item[1]})
# ............................................................
# upload image...............................................


def upload_image(request):
    categories = request.POST.get("Category")
    image = request.FILES["image_file"]
    update = Gallery(image=image, categories=categories)
    update.save()
    return render(request, "about_us/team.html")


def delete_image(request):
    id = request.POST.get("id")
    image = Gallery.objects.get(G_id=id)
    image.delete()
    return render(request, "about_us/team.html")
# ..............................................................

@user_passes_test(is_admin)
def image_upload_page_gallery(request):
    item = get_images()
    return render(request, "Gallery/upload_image.html", staff_detials(request,'Manage Gallery',{"categories": item[0], "images": item[1]}))
