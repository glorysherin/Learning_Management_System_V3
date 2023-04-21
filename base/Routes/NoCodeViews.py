from bs4 import BeautifulSoup
import htmlmin
import requests
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from ..models import Pages
from django.core.serializers import serialize
import json
from .Tool.Tools import random_image
import io
from django.http import FileResponse
# Create your views here.


def index(request):
    pages = Pages.objects.all()
    return render(request, 'NoCodeBuilderPages/pages.html', {"pages": pages})


def addPage(request):
    return render(request, 'NoCodeBuilderPages/index.html')


def savePage(request):
    if (request.method == 'POST'):
        html = request.POST['html']
        css = request.POST['css']
        Project_name = request.POST['Project_name']
        page = Pages.objects.create(
            name=Project_name, html=html, css=css, image=random_image())
        page.save()
    return JsonResponse({"result": (json.loads(serialize('json', [page])))[0]})


def editPage(request, id):
    page = Pages.objects.get(pk=id)
    return render(request, 'NoCodeBuilderPages/index.html', {"page": page})


def editPageContent(request, id):
    if (request.method == 'POST'):
        html = request.POST['html']
        css = request.POST['css']
        page = Pages.objects.get(pk=id)
        page.html = html
        page.css = css
        page.save()
    return JsonResponse({"result": (json.loads(serialize('json', [page])))[0]})


def previewPage(request, id):
    page = Pages.objects.get(pk=id)
    return render(request, 'NoCodeBuilderPages/preview.html', {"page": page})


def ResumeBuilder(request):

    return render(request, 'NoCodeBuilderPages/resume_maker.html')


def Own_Gpt(request):
    return render(request, 'gpt\index.html')


def chat_view(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        response = Code_scriping(prompt)
        chat_message = ChatMessage(prompt=prompt, response=response)
        chat_message.save()
        return JsonResponse({'bot': response})

    return render(request, 'gpt/index.html', {'chat_messages': ChatMessage.objects.all()})


def autogenerate(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        ProjectName = request.POST.get('ProjectName')
        print(query, ProjectName)
        a = Make_web(query, ProjectName)
        print("connected..........")
        code = a.create_page()
        print("buffering.....")
        buffer = io.BytesIO()
        buffer.write(code.encode('utf-8'))
        buffer.seek(0)
        # Generate a file name for the minified HTML file
        filename = 'Generated_code.html'

        # Create a FileResponse object with the minified HTML data and the specified filename
        response = FileResponse(
            buffer, as_attachment=True, filename=filename)

        return response
    return render(request, 'common/Autogenerate.html')


def url(request):
    return render(request, 'common/URL.html')


def Download_file(request):
    url = request.POST.get('text_area')
    response = requests.get(url)
    if request.method == 'POST':
        if 'Download' in request.POST:
            try:
                # Download webpage

                # Parse webpage using BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # Inline all JS and CSS into HTML
                for script in soup(['script', 'link']):
                    if script.has_attr('src'):
                        # Download and replace external JS and CSS with inline JS and CSS
                        if script.name == 'script':
                            content = requests.get(script['src']).text
                            script.string = content
                            script.attrs = {}
                        elif script.name == 'link' and script['rel'] == ['stylesheet']:
                            content = requests.get(script['href']).text
                            style = soup.new_tag('style', type='text/css')
                            style.string = content
                            script.replace_with(style)

                # Minify HTML
                minified_html = htmlmin.minify(str(soup))

                # Create a file-like buffer to receive the minified HTML data
                buffer = io.BytesIO()
                buffer.write(minified_html.encode('utf-8'))
                buffer.seek(0)

                # Generate a file name for the minified HTML file
                filename = 'minified.html'

                # Create a FileResponse object with the minified HTML data and the specified filename
                response = FileResponse(
                    buffer, as_attachment=True, filename=filename)

                return response
            except:
                return HttpResponse("The code is not open scorce")
    return render(request, 'common/URL.html')


def edits(request):
    return render(request, 'common/Edit.html')
