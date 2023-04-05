from django.shortcuts import render, redirect, get_object_or_404
from ..models import Faculty_details, Users, Sec_Daily_test_mark, Room, ClassRooms, class_enrolled, NoteCourse, Attendees, Student, Teacher, EbookForClass, daily_test
from django.contrib.auth.models import User
from .Tool.Tools import get_user_mail, get_user_name, get_user_role, get_user_obj
import datetime
from .Tool.Code_scriping_Tool import get_image_url
from .Forms.Notes_form import EbookClassForm
from base import models as TMODEL
from django.utils import timezone


def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


def nave_home_classroom(request, pk, class_id):
    if pk == "join":
        try:
            if class_enrolled.objects.filter(user_id=request.user.id, subject_code=class_id).exists():
                print("connection passed...")
            else:
                class_en = class_enrolled(
                    user_id=request.user.id, mail_id=get_user_mail(request), subject_code=class_id)
                class_en.save()
        except:
            if class_enrolled.objects.filter(user_id=request.user.id, subject_code=class_id).exists():
                print("connection passed...")
            else:
                class_en = class_enrolled(
                    user_id=request.user.id, mail_id=request.user.username, subject_code=class_id)
                class_en.save()
        peoples = []
        people = class_enrolled.objects.filter(subject_code=class_id)
        for i in people:
            print(i.class_id, i.mail_id)
            person_obj = User.objects.get(id=i.user_id)
            try:
                obj = Student.objects.get(user=person_obj)
                print(obj.role_no)
                peoples.append(obj)
            except:
                pass
                # obj = Teacher.objects.get(user=person_obj) if database are clear it will work properly
                # print(obj.role)
        detials = ClassRooms.objects.get(subject_code=class_id)

        # create new chat room..........

        if Room.objects.filter(name=class_id).exists():
            return render(request, 'class_room/classroom.html', {'people': peoples, "detail": detials})
        else:
            new_room = Room.objects.create(name=class_id)
            new_room.save()
            return render(request, 'class_room/classroom.html', {'people': peoples, "detail": detials})
    elif pk == "attendes":
        peoples = []
        people = class_enrolled.objects.filter(subject_code=class_id)
        for i in people:
            print(i.class_id, i.mail_id)
            person_obj = User.objects.get(id=i.user_id)
            try:
                obj = Student.objects.get(user=person_obj)
                print(obj.role_no)
                peoples.append(obj)
            except:
                pass
                # obj = Teacher.objects.get(user=person_obj) if database are clear it will work properly
                # print(obj.role)
        detials = ClassRooms.objects.get(subject_code=class_id)
        # print("users", [str(i.username) for i in peoples])
        return render(request, 'class_room/attendes.html', {'people': [[j, i] for i, j in enumerate(peoples)], "ids": [str(i.id) for i in peoples], "detail": detials, "date": datetime.datetime.now().date()})
    else:
        peoples = []
        people = class_enrolled.objects.filter(subject_code=class_id)
        test = class_enrolled.objects.all()
        detials = ClassRooms.objects.get(subject_code=class_id)

        for i in test:
            print(i.class_id, i.mail_id, i.subject_code)
        for i in people:
            print(i.class_id, i.mail_id, i.subject_code)
            person_obj = User.objects.get(id=i.user_id)
            try:
                obj = Student.objects.get(user=person_obj)
                print(obj.role_no)
                peoples.append(obj)
            except:
                pass
        books = EbookForClass.objects.filter(Class_id=class_id)
        if is_student(request.user):
            obj = User.objects.get(id=request.user.id)
            student_data = Student.objects.get(user=obj)
            if Room.objects.filter(name=class_id).exists():
                return render(request, 'class_room/student_class_room.html', {'student_data': student_data, 'people': peoples, "detail": detials, 'books': books})
            else:
                new_room = Room.objects.create(name=class_id)
                new_room.save()
                return render(request, 'class_room/student_class_room.html', {'student_data': student_data, 'people': peoples, "detail": detials, 'books': books})

        elif is_teacher(request.user):
            accountapproval = TMODEL.Teacher.objects.all().filter(
                user_id=request.user.id, status=True)
            if accountapproval:
                if Room.objects.filter(name=class_id).exists():
                    return render(request, 'class_room/staff_class_room.html', {'people': peoples, "detail": detials, 'books': books})
                else:
                    new_room = Room.objects.create(name=class_id)
                    new_room.save()
                    return render(request, 'class_room/staff_class_room.html', {'people': peoples, "detail": detials, 'books': books})
            else:
                return render(request, 'teacher/teacher_wait_for_approval.html')
        else:
            if Room.objects.filter(name=class_id).exists():
                return render(request, 'class_room/student_class_room.html', {'people': peoples, "detail": detials, 'books': books})
            else:
                new_room = Room.objects.create(name=class_id)
                new_room.save()
                return render(request, 'class_room/student_class_room.html', {'people': peoples, "detail": detials, 'books': books})


def home_classroom(request):
    classes = []
    img = {}
    dep = []
    sem = [1, 2, 3, 4, 5, 6, 7, 8]
    try:
        enroll_classes = class_enrolled.objects.filter(
            mail_id=get_user_mail(request))
        print(get_user_mail(request),
              "this is only passed now............\n\n\n\n\n\n\n\n")
    except:
        enroll_classes = class_enrolled.objects.filter(
            mail_id=request.user.email)
        print(str(request.user.email), "this is only passed now............\n\n\n\n\n\n\n\n",
              request.user.email)

    for i in enroll_classes:
        classrooms = ClassRooms.objects.filter(subject_code=i.subject_code)
        print(i.class_id)
        print(classrooms)
        for i in classrooms:
            print(i.id, i.class_name)
            classes.append(i)
            if i.department not in dep:
                dep.append(i.department)
    if is_student(request.user):
        classes = []
        try:
            enroll_classes = class_enrolled.objects.filter(
                mail_id=get_user_mail(request))
            print(get_user_mail(request),
                  "this is only passed now............\n\n\n\n\n\n\n\n")
        except:
            enroll_classes = class_enrolled.objects.filter(
                mail_id=request.user.username)

        for i in enroll_classes:
            classrooms = ClassRooms.objects.filter(subject_code=i.subject_code)
            print(i.class_id)
            print(classrooms)
            for i in classrooms:
                print(i.id, i.class_name)
                classes.append(i)
                if i.department not in dep:
                    dep.append(i.department)
        print("student is on ...")
        obj = User.objects.get(id=request.user.id)
        student_data = Student.objects.get(user=obj)
        try:
            return render(request, 'class_room/student_classroom.html', {'student_data': student_data, 'classes': classes, 'img': img, 'sem_': sem, 'dep': dep, "user_name": get_user_name(request), "User_role": get_user_role(request), "usr_img": get_user_obj(request)})
        except:
            return render(request, 'class_room/student_classroom.html', {'student_data': student_data, 'classes': classes, 'img': img, 'sem_': sem, 'dep': dep, "user_name": request.user.username})

    elif is_teacher(request.user):
        obj = User.objects.get(id=request.user.id)
        teacher_data = Teacher.objects.get(user=obj)
        teacher_data_1 = Faculty_details.objects.get(user_name=obj.username)
        accountapproval = TMODEL.Teacher.objects.all().filter(
            user_id=request.user.id, status=True)
        if accountapproval:
            try:
                return render(request, 'class_room/staff_classroom.html', {'detail': teacher_data_1, 'teacher_data': teacher_data, 'classes': classes, 'img': img, 'sem_': sem, 'dep': dep, "user_name": get_user_name(request), "User_role": get_user_role(request), "usr_img": get_user_obj(request)})
            except:
                return render(request, 'class_room/staff_classroom.html', {'teacher_data': teacher_data, 'classes': classes, 'img': img, 'sem_': sem, 'dep': dep, "user_name": request.user.username})
        else:
            return render(request, 'teacher/teacher_wait_for_approval.html')
    else:
        pass
        # try:
        #     return render(request, 'class_room/class_room_home.html', {'classes': classes, 'img': img, 'sem_': sem, 'dep': dep, "user_name": get_user_name(request), "User_role": get_user_role(request), "usr_img": get_user_obj(request)})
        # except:
        #     return render(request, 'class_room/class_room_home.html', {'classes': classes, 'img': img, 'sem_': sem, 'dep': dep, "user_name": request.user.username})


def add_class(request):
    return render(request, 'class_room/new_add.html')


def delete_class(request, room):
    class_room = ClassRooms.objects.get(id=room)
    class_room.delete()
    return render(request, 'class_room/new_add.html')


def save_add_class(request):
    class_name = request.POST.get('class_name')
    subject_code = request.POST.get('subject_code')
    department = request.POST.get('department')
    semester = request.POST.get('semester')
    discription = request.POST.get('discription')

    class_room = ClassRooms(class_image=get_image_url(class_name+" logos"), class_name=class_name, subject_code=subject_code,
                            department=department, semester=semester, discription=discription, owner=Faculty_details.objects.get(mail=get_user_mail(request)))
    class_room.save()
    class_id = ClassRooms.objects.get(subject_code=subject_code)
    enroll_class = class_enrolled(mail_id=get_user_mail(
        request), subject_code=subject_code, class_id=class_id.id)
    enroll_class.save()

    return render(request, 'class_room/new_add.html')


def edit_classroom(request, classroom_id):
    # Retrieve the classroom object from the database
    classroom = get_object_or_404(ClassRooms, subject_code=classroom_id)

    if request.method == 'POST':
        # Retrieve the updated data from the HTML form
        classroom.class_name = request.POST.get('class_name')
        classroom.subject_code = request.POST.get('subject_code')
        classroom.semester = request.POST.get('semester')
        classroom.department = request.POST.get('department')
        classroom.discription = request.POST.get('discription')
        classroom.class_image = request.POST.get('image_url')

        # Save the updated data to the database
        classroom.save()

        # Redirect to the detail view of the updated classroom
        return render(request, 'class_room/edit_class.html', {'classroom': classroom})

    # If the request method is not POST, render the edit form with the current data
    return render(request, 'class_room/edit_class.html', {'classroom': classroom})


def attendes(request):
    return render(request, 'class_room/attendes.html')


def update_attendes(request):
    my_date_time = timezone.now()
    data: str = []
    print("length is : ", request.POST.get('length'))
    for i in range(int(request.POST.get('length'))):
        datas = request.POST.get('#cars'+str(i))
        data.append(datas)
    for i in data:
        splited = i.split('~~')
        print(i.split('~~'), i)
        if Attendees.objects.filter(class_id=splited[2], roll_no=splited[3], Date=my_date_time).exists():
            print("Data Already Exists....")
        else:
            obj = Attendees(
                class_id=splited[2], user_name=splited[1], subject_states=splited[0], roll_no=splited[3]
            )
            obj.save()
        for i in Attendees.objects.all():
            print(i.user_name, i.subject_states)
    return render(request, 'class_room/attendes.html')


def update_edited_attendes(request):
    print("running..... update data")
    data: str = []
    print("length is : ", request.POST.get('length'))
    for i in range(int(request.POST.get('length'))):
        datas = request.POST.get('#cars'+str(i))
        data.append(datas)
    for i in data:
        splited = i.split('~~')
        print(i.split('~~'), i)
        obj = Attendees.objects.get(
            class_id=splited[2], roll_no=splited[3], user_name=splited[1])
        obj.subject_states = splited[0]
        obj.save()
        print(obj.class_id, obj.subject_states)
        print("updated....")
        print(
            f"states : states-{splited[0]}, classid = {splited[2]},roll_no:{splited[3]}")
    return render(request, 'class_room/attendes.html')


def edit_attendes_home(request):
    return render(request, 'class_room/edit_attendes_home.html')


def edit_attendes(request):
    class_id = request.GET.get('class_id')
    date = request.GET.get('date')
    for i in Attendees.objects.all():
        print(i.class_id, f"[{i.Date}]", i.user_name)
    attendees = Attendees.objects.filter(class_id=class_id, Date=date)
    context = {'attendees': [[i, j] for i, j in enumerate(attendees)]}
    print(context)
    return render(request, 'class_room/edit_attendes.html', context)


def view_attendes(request):
    class_id = request.GET.get('class_id')
    date = request.GET.get('date')
    for i in Attendees.objects.all():
        print(i.class_id, f"[{i.Date}]", i.user_name, i.subject_states)
    attendees = Attendees.objects.filter(class_id=class_id, Date=date)
    context = {'attendees': attendees}
    return render(request, 'class_room/sample.html', context)


def add_class_notes(request, pk):
    if request.method == 'POST':
        form = EbookClassForm(request.POST, request.FILES)
        if form.is_valid():
            ebook = form.save(commit=False)
            ebook.Class_id = pk
            ebook.cover_image = get_image_url(str(ebook.title)+" cover image")
            ebook.save()
            return redirect('course_list')
    else:
        form = EbookClassForm()
    return render(request, 'class_room/notes/add_notes.html', {'form': form, 'class_id': pk})


def class_ebook_edit(request, pk):
    ebook = get_object_or_404(EbookForClass, pk=pk)
    if request.method == 'POST':
        form = EbookClassForm(request.POST, request.FILES, instance=ebook)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = EbookClassForm(instance=ebook)
    return render(request, 'class_room/notes/ebook_edit.html', {'form': form})


def class_ebook_delete(request, pk):
    ebook = get_object_or_404(EbookForClass, pk=pk)
    ebook.delete()
    return redirect('course_list')


def class_book_list(request):
    books = EbookForClass.objects.all()
    return render(request, 'class_room/notes/ebook_list.html', {'books': books})


def mark(request, class_id):
    peoples = []
    people = class_enrolled.objects.filter(subject_code=class_id)
    for i in people:
        print(i.class_id, i.mail_id)
        person_obj = User.objects.get(id=i.user_id)
        try:
            obj = Student.objects.get(user=person_obj)
            print(obj.role_no)
            peoples.append(obj)
        except:
            pass
    detials = ClassRooms.objects.get(subject_code=class_id)
    courses = NoteCourse.objects.all()
    return render(request, "class_room/add_mark.html", {'courses': courses, 'people': [[j, i] for i, j in enumerate(peoples)], "ids": [str(i.id) for i in peoples], "detail": detials, "date": datetime.datetime.now().date()})


def update_mark(request):
    my_date_time = request.POST.get('#date')
    data: str = []
    for i in range(int(request.POST.get('length'))):
        datas = request.POST.get('#cars'+str(i))
        data.append(datas)
    for i in data:
        splited = i.split('~~')
        print(i.split('~~'), i)
        print(request.POST.get('#course'), my_date_time)
        if Sec_Daily_test_mark.objects.filter(class_id=splited[2], roll_no=splited[3], Date=my_date_time).exists():
            print("Data Already Exists....")
        else:
            obj = Sec_Daily_test_mark(
                class_id=splited[2], user_name=splited[1], mark=splited[0], roll_no=splited[3], Date=my_date_time, subject=request.POST.get(
                    '#course')
            )
            obj.save()
    return render(request, 'class_room/attendes.html')


def edit_mark_home(request):
    return render(request, 'class_room/edit_mark_home.html')


def edit_mark(request):
    class_id = request.GET.get('class_id')
    date = request.GET.get('date')
    for i in Sec_Daily_test_mark.objects.all():
        print(i.class_id, f"[{i.Date}]", i.user_name)
    attendees = Sec_Daily_test_mark.objects.filter(
        class_id=class_id, Date=date)
    courses = NoteCourse.objects.all()
    context = {'attendees': [[i, j]
                             for i, j in enumerate(attendees)], 'courses': courses, 'date': date}
    print(context)
    return render(request, 'class_room/edit_mark.html', context)


def update_edited_mark(request):
    print("running..... update data")
    data: str = []
    print("length is : ", request.POST.get('length'))

    for i in range(int(request.POST.get('length'))):
        datas = request.POST.get('#cars'+str(i))
        data.append(datas)
    for i in data:
        splited = i.split('~~')
        print(i.split('~~'), i)
        obj = Sec_Daily_test_mark.objects.get(
            class_id=splited[2], roll_no=splited[3], user_name=splited[1], Date=request.POST.get('#date'))
        obj.mark = splited[0]
        obj.subject = request.POST.get('#course')
        obj.save()
    return render(request, 'class_room/edit_mark.html')
