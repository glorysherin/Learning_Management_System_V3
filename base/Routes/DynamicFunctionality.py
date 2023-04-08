from ..models import Testimonials, FooterEditPage, SocialMediaLinks
from django.shortcuts import render
from .Tool.GeneralTools import reguler_datas


def Testimonicals(request):
    obj = Testimonials.objects.all()
    return render(request, "testimonials/Testimonicals.html", reguler_datas({"card": obj}))


def Testimonicals_edit(request):
    obj = Testimonials.objects.all()
    return render(request, "testimonials/Testimonicals_edit.html", reguler_datas({"card": obj}))


def Testimonicals_save(request):
    vals = ['#Name', '#position', '#description',
            '#Category', '#fileInput-single']
    Name = request.POST.get(vals[0])
    position = request.POST.get(vals[1])
    image = request.FILES[vals[-1]]
    description = request.POST.get(vals[2])
    categories = request.POST.get(vals[3])
    print("Working.....")
    vals = Testimonials(Name=Name, position=position, image=image,
                        description=description, categories=categories)
    vals.save()

    return render(request, "testimonials/Testimonicals_edit.html", reguler_datas())


# Footer ......................
def footer_edit(request):
    return render(request, "footer_edit.html", reguler_datas({'FooterEditPage': FooterEditPage.objects.all()[::-1], 'SocialMediaLinks': SocialMediaLinks.objects.all()[::-1]}))


def FooterEditPage_save(request):
    InstituteName = request.POST.get("#Institute_Name")
    Address = request.POST.get("#Address")
    PhoneNumber = request.POST.get("#Phone_Number")
    EXN = request.POST.get("#EXN")
    mail = request.POST.get("#EmailId")

    obj = FooterEditPage(InstituteName=InstituteName, Address=Address,
                         PhoneNumber=PhoneNumber, EXN=EXN, mail=mail)
    obj.save()

    return render(request, "footer_edit.html", reguler_datas())


# SocialMediaLinks......................
def SocialMediaLinks_save(request):
    Twitter = request.POST.get("#Twitter_link")
    Facebook = request.POST.get("#Facebook_Link")
    Instagram = request.POST.get("#Instagram_Link2")
    LinkedIn = request.POST.get("#LinkedIn_Link")
    obj = SocialMediaLinks(Twitter=Twitter, Facebook=Facebook,
                           Instagram=Instagram, LinkedIn=LinkedIn)
    obj.save()
    return render(request, "footer_edit.html", reguler_datas())
