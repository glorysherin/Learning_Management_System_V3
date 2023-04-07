from django.shortcuts import render, redirect
from ..models import Faculty_details, Users, Teacher, ClassRooms, class_enrolled, Student
from django.contrib.auth.models import User


def add_faculty(request):
    facultys = Faculty_details.objects.all()
    for i in facultys:
        print(i.name)
    return render(request, "admin/Admin_page_to_add_Facuilty.html", {'users': facultys})


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


def teacher_profile(request, pk):
    # teacher = get_object_or_404(Teacher, id=pk)
    teacher = Teacher.objects.get(id=pk)
    return render(request, 'admin_actions/teacher_profile.html', {'teacher': teacher})

# classes


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
    return render(request, 'admin_actions/class_list.html', context)


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
