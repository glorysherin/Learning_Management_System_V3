import openai
from django.shortcuts import get_object_or_404
from ...models import Faculty_details, Student, Users, Teacher, Notifications, BotControl
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
import requests
import random


def random_image():
    # URL of website with SVG images
    url = "https://www.google.com/search?q=nocode+svg+images&tbm=isch&ved=2ahUKEwj0j47uy6v-AhVc1HMBHQtXBaYQ2-cCegQIABAA&oq=nocode+svg+images&gs_lcp=CgNpbWcQAzoKCAAQigUQsQMQQzoHCAAQigUQQzoFCAAQgARQrQNYjAtgyw1oAHAAeACAAacCiAHoC5IBBTAuNC40mAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=73A6ZLTcItyoz7sPi66VsAo&bih=760&biw=1536&rlz=1C1RXQR_enIN1038IN1038"

    # Make a GET request to the URL and get the HTML content
    response = requests.get(url)
    html_content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    image_urls = []
    
    # Find all image tags and extract the URLs
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if img_url and img_url.startswith('http'):
            image_urls.append(img_url)

    # Choose a random image URL from the list
    return random.choice(image_urls)



def get_user_mail(request):
    usr_id = request.user.id
    usr_obj = User.objects.get(id=usr_id)
    faculty_details = Faculty_details.objects.get(mail=usr_obj.username)
    return faculty_details.mail


def get_user_name(request):
    usr_id = request.user.id
    usr_obj = User.objects.get(id=usr_id)
    faculty_details = Faculty_details.objects.get(mail=usr_obj.username)
    return faculty_details.user_name

def get_user_name_byid(usr_id):
    usr_obj = User.objects.get(id=usr_id)
    faculty_details = Faculty_details.objects.get(mail=usr_obj.username)
    return faculty_details.user_name

def get_user_obj(request):
    usr_id = request.user.id
    usr_obj = User.objects.get(id=usr_id)
    faculty_details = Faculty_details.objects.get(mail=usr_obj.username)
    return faculty_details


def get_user_role(request):
    usr_id = request.user.id
    usr_obj = User.objects.get(id=usr_id)
    faculty_details = Faculty_details.objects.get(mail=usr_obj.username)
    if faculty_details.role.role == 1:
        return "Admin"
    elif faculty_details.role.role == 2:
        return "Hod"
    elif faculty_details.role.role == 3:
        return "staff"
    elif faculty_details.role.role == 4:
        return "Student"


def remove_space(string):
    out = ""
    for i in string:
        if i != " ":
            out = out + i
    return out


def gpt(queary):
    openai.api_key = "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"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=queary,
        temperature=0.5,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
        stop=["You:"]
    )
    return response.choices[0].get("text")


def student_detials(request, page, dict_inp={}):
    usr_id = request.user.id
    usr_obj = User.objects.get(id=usr_id)
    try:
        bot = BotControl.objects.filter(usr_id=request.user.id)[::-1][0].toggle
    except:
        bot = 0
    print("working..... role : ",get_current_user_role(request))
    if get_current_user_role(request) == 1:
        dict_={
            'usr': usr_obj,
            'page':page,
            'usr_role':get_current_user_role(request)
        }
    elif get_current_user_role(request) == 2 or get_current_user_role(request) == 3:
        dict_={
            'usr': usr_obj,
            'page':page,
            'usr_role':get_current_user_role(request) 
        }
    else:
        print("student")
        std_data = Student.objects.get(user=usr_obj)
        dict_ = {
            'usr': std_data,
            'page': page,
            'usr_role':4
        }
    not_obj =  Notifications.objects.filter(to_user=request.user.id)
    dict_ = {**dict_,"notification":not_obj,'bot':bot}
    print(dict_)
    return {**dict_, **dict_inp}


def staff_detials(request, page, dict_inp={}):
    usr_id = request.user.id
    try:
        bot = BotControl.objects.filter(usr_id=request.user.id)[::-1][0].toggle
    except:
        bot = 0
    usr_obj = User.objects.get(id=usr_id)
    name = Users.objects.get(user_name=usr_obj.username)
    faculty_details = Faculty_details.objects.get(user_name=name.user_name)
    teacher_role=Teacher.objects.get(user=usr_obj)
    role = teacher_role.role
    print(teacher_role)
    dict_ = {
        'stusr': faculty_details,
        'page': page,
        'staff_name': faculty_details.name,
        'role': role,
        'pro_id':teacher_role
    }
    not_obj =  Notifications.objects.filter(to_user=request.user.id)
    dict_ = {**dict_,"notification":not_obj,'bot':bot}
    return {**dict_, **dict_inp}

def get_current_user_role(request):
    obj = User.objects.get(id=request.user.id)
    get_role = Users.objects.get(user_name=obj.username).role
    return get_role

