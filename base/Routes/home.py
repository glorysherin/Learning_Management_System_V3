from django.shortcuts import render
from .Tool.blogTool import get_images


# from django.core.mail import send_mail
# from django.conf import settings
# import smtplib
# import ssl
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart


def pre_home(request):
    item = get_images()
    # sender_email = settings.EMAIL_HOST_USER
    # password = settings.EMAIL_HOST_PASSWORD
    # message = MIMEMultipart("alternative")
    # message["Subject"] = "Testing App"
    # message["From"] = sender_email
    # context = ssl.create_default_context()
    # server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
    # server.ehlo()
    # server.login(sender_email, password)
    # subject = 'welcome to GFG world'
    # message = f'Hi nagi, thank you for registering in geeksforgeeks.'
    # email_from = settings.EMAIL_HOST_USER
    # recipient_list = ["nagipragalathan@gmail.com", ]
    # send_mail( subject, message, email_from, recipient_list )

    return render(request, 'pre_home/index.html', {"categories": item[0], "images": item[1]})


def contactus(request):
    return render(request, 'pre_home/contactus.html')


def services(request):
    return render(request, 'pre_home/services.html')


def about(request):
    return render(request, 'pre_home/about.html')

def parentsession(request):
    return render(request, 'pre_home/parentsession.html')
