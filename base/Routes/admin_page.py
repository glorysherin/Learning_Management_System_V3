from django.shortcuts import render, redirect, get_object_or_404
from ..models import Faculty_details, Users, Teacher, ClassRooms, class_enrolled, Student, Attendees, Note, Department,SocialMedia, BotControl
from django.contrib.auth.models import User
from django.http import HttpResponse
import xlwt
from .Tool.Tools import student_detials, staff_detials
from .study import is_admin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse



def add_faculty(request):
    facultys = Faculty_details.objects.all()
    for i in facultys:
        print(i.name)
    return render(request, "admin/Admin_page_to_add_Facuilty.html", {'users': facultys})

def manage_lms(request):
    return render(request, "admin_actions/manage_lms.html")


def add_usr(request):
    usr_name = request.POST.get('user_name')
    password = request.POST.get('mail')
    role = request.POST.get('roles')
    mail = request.POST.get('password')

    facultys = Faculty_details.objects.all()
    for i in facultys:
        print(i.name)
    try:
        add_user = Users(user_name=usr_name, mail_id=mail,
                         password=password, role=role)
        add_user.save()
        current_user = Users.objects.get(mail_id=mail)
        Fac_del = Faculty_details(user_name=usr_name, mail=mail,
                                  role=current_user, id_number=0, name=add_user.user_name)
        Fac_del.save()
        user = User.objects.create_user(mail, usr_name, password)
        user.save()
    except:
        print("unique are missed....")
    return render(request, "admin/Admin_page_to_add_Facuilty.html", {'users': facultys})


def add_facu(request):
    facultys = Faculty_details.objects.all()
    for i in facultys:
        print(i.name)
    return render(request, "dashboard/tables.html", {'users': facultys})


def teachers(request):
    teachers = Teacher.objects.all()
    departments = set(teacher.department for teacher in teachers)
    context = {
        'teachers': teachers,
        'departments': departments,
    }
    return render(request, 'admin_actions/list_teacher.html', context)


def teacher_profile(request, staff_id):
    # teacher = get_object_or_404(Teacher, id=pk)
    teacher = Teacher.objects.get(id=staff_id)
    try:
        links = SocialMedia.objects.get(std_id=request.user.id)
    except:
        links=None
    return render(request, 'admin_actions/teacher_profile.html', staff_detials(request, teacher.role+' Profile', {'links':links,'teacher': teacher,'teacher_id':teacher.id}))

# classes
 
@user_passes_test(is_admin)
def class_list(request):
    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        if class_id:
            class_obj = ClassRooms.objects.get(id=class_id)
            class_obj.delete()
            return redirect('class_list')

    semesters = set(
        [classroom.semester for classroom in ClassRooms.objects.all()])
    departments = set(
        [classroom.department for classroom in ClassRooms.objects.all()])
    class_dict = {}
    for semester in semesters:
        class_dict[semester] = {}
        for department in departments:
            classes = ClassRooms.objects.filter(
                semester=semester, department=department)
            class_dict[semester][department] = classes

    context = {'class_dict': class_dict}
    return render(request, 'admin_actions/class_list.html', staff_detials(request,'Class Details',context))


def get_class_peoples(request, class_id):
    peoples = []
    people = class_enrolled.objects.filter(subject_code=class_id)
    test = class_enrolled.objects.all()
    for i in test:
        print(i.class_id, i.mail_id, i.subject_code)
    for i in people:
        print(i.class_id, i.mail_id, i.subject_code)
        person_obj = User.objects.get(id=i.user_id)
        try:
            obj = Student.objects.get(user=person_obj.id)
            print(obj.role_no)
            peoples.append(obj)
        except:
            pass
    print(peoples)
    return render(request, 'admin_actions/list_users.html', {"people": peoples})


def class_dates(request):
    class_ids = Attendees.objects.values('class_id').distinct()
    class_dates = {}
    for class_id in class_ids:
        dates = Attendees.objects.filter(
            class_id=class_id['class_id']).dates('Date', 'day')
        class_dates[class_id['class_id']] = dates
    context = {'class_dates': class_dates}
    return render(request, 'admin_actions/class_dates.html', context)


def user_details(request, class_id, date):
    attendees = Attendees.objects.filter(class_id=class_id, Date=date)
    context = {'attendees': attendees}
    return render(request, 'admin_actions/user_details.html', context)


def delete_attendee(request, id):
    attendee = Attendees.objects.get(pk=id)
    attendee.delete()
    return redirect('class_dates')


def edit_attendee(request, id):
    attendee = get_object_or_404(Attendees, id=id)

    if request.method == 'POST':
        class_id = request.POST.get('class_id')
        user_name = request.POST.get('username')
        roll_no = request.POST.get('rollno')
        subject_states = request.POST.get('status')

        # attendee.class_id = class_id
        attendee.user_name = user_name
        attendee.roll_no = roll_no
        attendee.subject_states = subject_states

        attendee.save()

        return redirect('class_dates')

    context = {'attendee': attendee}
    return render(request, 'admin_actions/edit_attendes.html', context)


def export_attendees(request, class_id, date, date_):
    attendees = Attendees.objects.filter(class_id=class_id, Date=date)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename={class_id}_{date}.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Attendees')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['ID', 'Class ID', 'User Name',
               'Roll No', 'Subject Status', 'Date']
    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title, font_style)
    rows = attendees.values_list(
        'id', 'class_id', 'user_name', 'roll_no', 'subject_states', 'Date')
    for row in rows:
        row_num += 1
        for col_num, cell_value in enumerate(row):
            ws.write(row_num, col_num, str(cell_value), font_style)
    wb.save(response)
    return response


def listout_notes(request):
    departments = set([note.department for note in Note.objects.all()])
    notes_dict = {}
    for department in departments:
        notes = Note.objects.filter(department=department).exclude(semester='')
        semesters = set([note.semester for note in notes])
        notes_dict[department] = {}
        for semester in semesters:
            notes_dict[department][semester] = Note.objects.filter(
                department=department, semester=semester)
    return render(request, 'admin_actions/notes_list.html', {'notes_dict': notes_dict})


def teacher_list(request):
    staff = Teacher.objects.filter(role='staff')
    return render(request, 'admin_actions/teacher_list.html',staff_detials(request,'Staff Details',{'teachers': staff}))

def hod_list(request):
    hod = Teacher.objects.filter(role='hod')
    return render(request, 'admin_actions/teacher_list.html',staff_detials(request,'Hod Details',{'teachers': hod}))

def admin_list(request):
    teachers = Teacher.objects.filter(role='admin')
    return render(request, 'admin_actions/admin_list.html',{'teachers': teachers})


def teacher_delete(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    teacher.delete()
    return redirect('teacher_list')




def teacher_edit(request, teacher_id):
    teacher = Teacher.objects.get(id=teacher_id)
    department = Department.objects.all()
    if request.method == 'POST':
        print(request.POST.get('department'))
        teacher.user.first_name = request.POST.get('first_name')
        teacher.user.last_name = request.POST.get('last_name')
        teacher.address = request.POST.get('address')
        teacher.mobile = request.POST.get('mobile')
        teacher.role = request.POST.get('role')
        teacher.status = request.POST.get('status') == 'on' 
        teacher.department = request.POST.get('department')
        teacher.salary = request.POST.get('salary')
        teacher.Annauni_num = request.POST.get('Annauni_num')
        teacher.save()
        print("datas are updated....")
        teacher = Teacher.objects.get(id=teacher_id)
        print(teacher.department)

        return render(request, 'attandees/teacher_edit_message.html',{'id':teacher_id})

    return render(request, 'admin_actions/teacher_edit.html', staff_detials(request,"Edit profile",{'teacher': teacher,'dep':department}))

# def teacher_edit_msg(request):
#     return render(request, 'attandees/teacher_edit_message.html')


def handle_toogle(request,action):
    # Create a dictionary or any data structure containing the JSON response
    obj = BotControl(usr_id=request.user.id,toggle=action)
    obj.save()
    data = {
        'message': action,
        'status': 'success'
    }
    
    # Return the JSON response using JsonResponse
    return JsonResponse(data)

