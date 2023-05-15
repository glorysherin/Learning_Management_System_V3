import pywhatkit as kit
from django.conf import settings
from django.shortcuts import render, redirect
from googletrans import Translator, LANGUAGES
from django.http import HttpResponse
from gtts import gTTS
from langdetect import detect
import os
import io
from LMS.settings import BASE_DIR
import wikipedia
from docx2pdf import convert
from django.core.files.storage import default_storage
from pdf2docx import parse
import tabula
import pandas as pd
from openpyxl import load_workbook
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from PIL import Image
import tempfile
import requests
from random import choice
from docx import Document
from django.http import JsonResponse
from docx.shared import Inches
from googlesearch import search
from bs4 import BeautifulSoup
from .Tool.Code_scriping_Tool import get_image_url
from .Tool.Tools import student_detials, staff_detials

from .Tool.Code_scriping_Tool import get_stackoverflow_link, get_stackoverflow_link_1, get_example_code_gfg, get_answer_from_given_link


def toolHome(request):
    return render(request, "tools/ToolHome.html", student_detials(request, 'Tools-Home'))


def Code_scriping(request):
    context = {}
    if request.method == 'POST':
        question = request.POST.get('question')
        if question:
            # Get the Stack Overflow link for the question
            link = get_stackoverflow_link_1(question)
            link_gfg = get_stackoverflow_link_1(question, 'geeksforgeeks.org')
            if link:
                # Get the example code from the link
                code = get_answer_from_given_link(link)
                code_gfg = get_example_code_gfg(link_gfg)
                if code:
                    # Add the question, link and code to the context
                    context['question_s'] = question
                    context['link_s'] = link
                    context['code_s'] = code
                else:
                    context['error'] = 'No example code found for the given question'
                if code_gfg:
                    # Add the question, link and code to the context
                    context['question_gfg'] = question
                    context['link_gfg'] = link
                    context['code_gfg'] = code_gfg
            else:
                context['error'] = 'No result Found'
        else:
            context['error'] = 'Please enter a question'
    return render(request,  'tools/CodeScriping.html', student_detials(request, 'Code Scrapping', context))


def calculator(request):
    return render(request, 'tools/calculator.html',student_detials(request, 'Calculator'))


def translate_(request):
    text = request.POST.get('text')
    source_lang = request.POST.get('source_lang')
    target_lang = request.POST.get('target_lang')
    print(source_lang, target_lang)
    try:
        translator = Translator()
        translation = translator.translate(
            text, src=source_lang, dest=target_lang)
    except:
        translation = ""
    context = {
        'text': text,
        'src_lang': source_lang,
        'dest_lang': target_lang,
        'translation': translation,
        'LANGUAGES': LANGUAGES
    }
    return render(request, 'tools/translate.html', student_detials(request, 'Transulator', context))


def convert_text(request):
    if request.method == 'POST':
        filename = os.path.join(
            BASE_DIR, "generated_files/audio_files/output.mp3")
        os.remove(filename)
        text = request.POST['text']
        language = detect(text)
        tts = gTTS(text=text, lang=language)
        tts.save(filename)
        with open(filename, 'rb') as f:
            response = HttpResponse(f.read(), content_type='audio/mpeg')
            response['Content-Disposition'] = 'attachment; filename="output.mp3"'
            return response
    return render(request, 'tools/text_to_audio.html', student_detials(request, 'convert_text'))


def wikipedia_summary(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        sentence = request.POST.get('sentence')

        try:
            summary = wikipedia.summary(keyword, sentences=sentence)
            if request.POST.get('action') == 'view':
                return render(request, 'tools/wikipedia_summary.html', student_detials(request, 'keyword to para',{"summary": summary}))
            elif request.POST.get('action') == 'download':
                response = HttpResponse(summary, content_type='text/plain')
                response['Content-Disposition'] = f'attachment; filename="{keyword}.txt"'
                return response
        except wikipedia.exceptions.PageError:
            return HttpResponse("Page not found!")
        except wikipedia.exceptions.DisambiguationError as e:
            return HttpResponse("Disambiguation Error!")
    else:
        return render(request, 'tools/wikipedia_summary.html', student_detials(request, 'keyword to para'))


def convert_docx_to_pdf(request):
    if request.method == 'POST' and request.FILES['docx_file']:
        docx_file = request.FILES['docx_file']
        filename = docx_file.name
        with open(filename, 'wb+') as f:
            for chunk in docx_file.chunks():
                f.write(chunk)
        convert(filename)
        name_without_extension = os.path.splitext(filename)[0]
        pdf_path = name_without_extension + '.pdf'
        docx_path = name_without_extension + '.docx'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{pdf_path}"'
        with open(pdf_path, 'rb') as f:
            response.write(f.read())
        os.remove(pdf_path)
        os.remove(docx_path)
        return response
    else:
        return render(request, 'tools/convert_docx_to_pdf.html', student_detials(request, 'Docx to Pdf'))


def convert_pdf_to_docx(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        filename = default_storage.save('tmp/' + pdf_file.name, pdf_file)

        # convert the pdf file to docx format
        docx_file = io.BytesIO()
        parse(os.path.join('media', filename), docx_file)
        docx_file.seek(0)

        response = HttpResponse(docx_file.read(
        ), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename=' + \
            pdf_file.name.split('.')[0] + '.docx'

        default_storage.delete(filename)

        return response

    return render(request, 'tools/convert_pdf_to_docx.html', student_detials(request, 'Pdf to Docx'))


def convert_pdf_to_excel(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        # get the uploaded PDF file
        pdf_file = request.FILES['pdf_file']
        # convert the PDF file into a list of lists
        tables = tabula.read_pdf(pdf_file, pages='all', multiple_tables=True)
        # convert the list of lists into a DataFrame
        df = pd.DataFrame(tables[0])
        # save the DataFrame as an Excel file
        df.to_excel('output.xlsx', index=False)
        # send the Excel file to the user for download
        with open('output.xlsx', 'rb') as excel_file:
            response = HttpResponse(
                excel_file.read(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=output.xlsx'
            return response
    else:
        return render(request, 'tools/convert_pdf_to_excel.html', student_detials(request, 'Pdf to Excel'))


def convert_excel_to_pdf(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        wb = load_workbook(excel_file, read_only=True)
        ws = wb.active
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        c.setFont('Helvetica', 12)
        x, y = 1 * inch, 10.5 * inch
        for row in ws.iter_rows():
            for cell in row:
                cell_value = cell.value
                if cell_value is None:
                    cell_value = ''
                else:
                    cell_value = str(cell_value)
                c.drawString(x, y, cell_value)
                x += 1 * inch
            x = 1 * inch
            y -= 0.5 * inch
        c.save()
        pdf_buffer.seek(0)
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="output.pdf"'

        return response

    return render(request, 'tools/convert_excel_to_pdf.html',student_detials(request, 'Excel to Pdf'))


def convert_images_to_pdf(images):
    filename = tempfile.mktemp(".pdf")
    c = canvas.Canvas(filename)
    for image in images:
        img = Image.open(image)
        width, height = img.size
        c.setPageSize((width, height))
        c.drawImage(image, 0, 0, width, height)
        c.showPage()
        img.close()
    c.save()
    return filename


def convert_jpg_to_pdf(request):
    if request.method == 'POST':
        files = request.FILES.getlist('file')
        if len(files) == 0:
            return HttpResponse("No images selected")
        temp_dir = tempfile.mkdtemp()
        for f in files:
            with open(os.path.join(temp_dir, f.name), 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

        # Convert images to PDF
        pdf_file = convert_images_to_pdf(
            [os.path.join(temp_dir, f.name) for f in files])

        # Serve the PDF file for download
        with open(pdf_file, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=converted.pdf'
            return response

        # Delete temporary files
        shutil.rmtree(temp_dir)

    return render(request, 'tools/convert_jpg_to_pdf.html',student_detials(request,'convert jpg to pdf'))


def convert_jpg_to_word(request):
    if request.method == 'POST' and request.FILES['files']:
        # Get the uploaded images
        images = request.FILES.getlist('files')

        # Create a new Word document
        document = Document()

        # Loop through the images and add them to the document
        for img in images:
            # Open the image and convert it to a stream
            image = Image.open(img)
            stream = io.BytesIO()
            image.save(stream, format='png')
            stream.seek(0)

            # Add the image to the document
            document.add_picture(stream, width=Inches(6))

        # Save the document
        filename = 'images.docx'
        document.save(filename)

        # Download the document
        with open(filename, 'rb') as f:
            response = HttpResponse(f.read(
            ), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = 'attachment; filename={}'.format(
                filename)
            return response

    return render(request, 'tools/convert_jpg_to_word.html',student_detials(request,'convert jpg to word'))


def cgpa_calculator(request):
    if request.method == 'POST':
        total_credits = 0
        total_weighted_points = 0
        for i in range(1, 9):  # Assuming a maximum of 8 subjects
            credit_field = 'credit' + str(i)
            grade_field = 'grade' + str(i)
            credits = int(request.POST.get(credit_field, 0))
            grade_points = get_grade_points(request.POST.get(grade_field, ''))
            total_credits += credits
            total_weighted_points += credits * grade_points
        try:
            cgpa = round(total_weighted_points / total_credits, 2)
            context = {'cgpa': cgpa, 'len': [i for i in range(1, 10)]}
        except:
            context = {'cgpa': 'cgpa', 'len': [i for i in range(1, 10)]}
            print("error/...")
        return render(request, 'tools/cgpa_calculator.html', context)
    else:
        return render(request, 'tools/cgpa_calculator.html', context)


def get_grade_points(grade):
    if grade == 'S':
        return 10
    elif grade == 'A':
        return 9
    elif grade == 'B':
        return 8
    elif grade == 'C':
        return 7
    elif grade == 'D':
        return 6
    elif grade == 'E':
        return 5
    else:
        return 0


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def get_subject(request):
    if request.method == 'POST':
        num = request.POST.get('number')
        return render(request, 'tools/gpa_calculator.html', student_detials(request,'Select the Subjects to Calculet',{'num_sub': [i for i in range(1, int(num)+1)]}))

    return render(request, 'tools/num_of_sub.html',student_detials(request,'Select the Subjects to Calculet'))


def gpa_calculator(request):
    credits = request.POST.getlist('credits')
    grades = request.POST.getlist('grades')

    total_credits = sum(map(int, credits))
    total_grade_points = 0

    for i in range(len(credits)):
        grade_point = 0
        if grades[i] == 'A+':
            grade_point = 4.0
        elif grades[i] == 'A':
            grade_point = 4.0
        elif grades[i] == 'A-':
            grade_point = 3.7
        elif grades[i] == 'B+':
            grade_point = 3.3
        elif grades[i] == 'B':
            grade_point = 3.0
        elif grades[i] == 'B-':
            grade_point = 2.7
        elif grades[i] == 'C+':
            grade_point = 2.3
        elif grades[i] == 'C':
            grade_point = 2.0
        elif grades[i] == 'C-':
            grade_point = 1.7
        elif grades[i] == 'D+':
            grade_point = 1.3
        elif grades[i] == 'D':
            grade_point = 1.0
        elif grades[i] == 'F':
            grade_point = 0.0
        total_grade_points += int(credits[i]) * grade_point
    try:
        gpa = total_grade_points / total_credits
    except:
        gpa = 0.0
    context = {'gpa': round(gpa, 2)}    
    return render(request, 'tools/gpa_calculator.html', student_detials(request, 'Gpa Calculator', context))
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


def handwriting_converter(request):
    if request.method == 'POST':
        # Get input text from form
        input_text = request.POST.get('input_text')

        # Create a filename for the image
        filename = 'handwriting.png'

        # Generate image using Pywhatkit
        kit.text_to_handwriting(input_text, os.path.join(
            settings.MEDIA_ROOT, filename))

        # Open image file
        with open(os.path.join(settings.MEDIA_ROOT, filename), 'rb') as f:
            response = HttpResponse(f.read(), content_type="image/png")
            response['Content-Disposition'] = 'attachment; filename=' + filename
            return response
    else:
        return render(request, 'tools/handwriting.html', student_detials(request, 'Text to Hand Written'))


def keyword_to_image(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        print(keyword,'keyword')
        urls = get_image_url(keyword)
        print(keyword, urls)
        return render(request, 'tools/keyword_to_image.html', student_detials(request, 'keyword to image',{'image_urls': urls}))
    return render(request, 'tools/keyword_to_image.html', student_detials(request, 'keyword to image'))

# views.py


def join_meeting(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        return redirect('video_meeting', room_id=room_id)
    return render(request, 'tools/join_meeting.html', student_detials(request, 'Join Meeting', {}))


def staff_join_meeting(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        return redirect('staff_meeting', room_id=room_id)
    return render(request, 'tools/staff_join_meeting.html', staff_detials(request, 'Join Meeting', {}))


def admin_join_meeting(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        return redirect('admin_meeting', room_id=room_id)
    return render(request, 'tools/admin_join_meeting.html')


def meeting(request, room_id):
    context = {
        'room_id': room_id,
    }
    return render(request, 'tools/video_meeting.html', student_detials(request, 'Meeting', context))


def staff_meeting(request, room_id):
    context = {
        'room_id': room_id,
    }
    return render(request, 'tools/staff_video_meeting.html', staff_detials(request, 'Meeting', context))


def admin_meeting(request, room_id):
    context = {
        'room_id': room_id,
    }
    return render(request, 'tools/admin_video_meeting.html', context)


def common_join_meeting(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        return redirect('common_meeting', room_id=room_id)
    return render(request, 'student/meeting.html', student_detials(request, 'Join Meeting', {}))


def common_meeting(request, room_id):
    context = {
        'room_id': room_id,
    }
    return render(request, 'tools/video_meeting.html', context)


def Common_tool(request):
    return render(request, "tools/Common_tool.html")

# def get_stackoverflow_link(question, site='stackoverflow.com'):

#     num_results = 50

#     stackoverflow_link = ""
#     # Search Google for the question and get the top search results
#     search_results = search(question, num_results=num_results)

#     # Loop through the search results and find the Stack Overflow link
#     for result in search_results:
#         if site in result:
#             stackoverflow_link = result
#             break

#     return stackoverflow_link

# def get_example_code_gfg(url):
#     code = ""
#     # Send a GET request to the URL
#     response = requests.get(url)

#     # Parse the HTML content of the page using BeautifulSoup
#     soup = BeautifulSoup(response.content, 'html.parser')

#     # Find the div element containing the example code
#     example_code_div = soup.find_all('div', {'class': 'container'})
#     print("for lop")
#     for i in example_code_div:
#         code = code + str(i)
#     # Get the text content of the example code div
#     # example_code = example_code_div.get_text()
#     # Return the example code
#     return code
conversation = {"hello":["hello","hey, hello how can i help you"],"who are you":["i am lms chatbot"," am a chatbot"],"how are you":["I'm great, thank you! How can I assist you today?" ,"I'm great, thank you!"],"what's the weather like today":["The weather is sunny and warm today. It's a perfect day to go outside!"],"How can I reset my password?":["To reset your password, you can go to the login page and click on the 'Forgot Password'."],"what are the tools available":['''<ul>
  <li>User Management</li>
  <li>Course Management</li>
  <li>Content Management</li>
  <li>Learning Material Access</li>
  <li>Assessment and Grading</li>
  <li>Communication Tools</li>
  <li>Progress Tracking</li>
</ul>
'''],"who are the lms  developers":['''<ul>
  <li> <img style="width:40px;border-radius:80px;height:40px" src="data:image/jpeg;base64,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" alt="User Management"> <a href="https://github.com/NagiPragalathan">  Nagi Pragalathan</a></li>
  <li><a href="https://github.com/jkokilaCSE">Kokila</a></li>
  <li><a href="https://github.com/glorysherin">Glory Sherin</a></li>
  <li><a href="https://github.com/MohanKumarMurugan">Mohan Kumar</a></li>
</ul>
''']}
def chatbot_res(request):
    if request.method == "GET":
        message = request.GET.get("message")
        print(message)
        if message in conversation.keys():
            code = choice(conversation.get(message))
        else:
            link = get_stackoverflow_link(message)
            code = get_answer_from_given_link(link)
        if code:
            response = code
        else:
            wikipedia.set_lang("en")
            # Get the summary of a page
            page = wikipedia.page(message)
            summary = page.summary
            response = summary
        return JsonResponse({"response": response})
    else:
        return JsonResponse({"error": "Invalid request method"})
