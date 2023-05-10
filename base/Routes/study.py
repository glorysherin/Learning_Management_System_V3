import requests
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from ..models import Users, Faculty_details, Internal_test_mark, Course, Sec_Daily_test_mark, Room, ClassRooms, class_enrolled, NoteCourse, Attendees, Student, Teacher, EbookForClass, daily_test
from django.contrib.auth.models import User
from .Tool.Tools import get_user_mail, get_user_name, get_user_role, get_user_obj
import datetime
from datetime import datetime
from .Tool.Code_scriping_Tool import get_image_url
from .Forms.Notes_form import EbookClassForm
from base import models as TMODEL
from django.utils import timezone
from googlesearch import search
import urllib.parse

from bs4 import BeautifulSoup

from .Tool.Tools import student_detials, staff_detials


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
        obj = User.objects.get(id=request.user.id)
        get_role = Users.objects.get(user_name=obj.username)
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
                return render(request, 'class_room/student_class_room.html', {'student_data': student_data, 'people': peoples, "detail": detials, 'books': books, 'recent_books': books[::-1][0:4]})
            else:
                new_room = Room.objects.create(name=class_id)
                new_room.save()
                return render(request, 'class_room/student_class_room.html', {'student_data': student_data, 'people': peoples, "detail": detials, 'books': books, 'recent_books': books[::-1][0:4]})

        elif is_teacher(request.user):
            accountapproval = TMODEL.Teacher.objects.all().filter(
                user_id=request.user.id, status=True)
            if accountapproval:
                if Room.objects.filter(name=class_id).exists():
                    return render(request, 'class_room/staff_class_room.html', {'people': peoples, "detail": detials, 'books': books, 'recent_books': books[::-1][0:4]})
                else:
                    new_room = Room.objects.create(name=class_id)
                    new_room.save()
                    return render(request, 'class_room/staff_class_room.html', {'people': peoples, "detail": detials, 'books': books, 'recent_books': books[::-1][0:4]})
            else:
                return render(request, 'teacher/teacher_wait_for_approval.html')
        if get_role.role == 1:
            return render(request, 'class_room/staff_class_room.html', {'people': peoples, "detail": detials, 'books': books, 'recent_books': books[::-1][0:4]})
        else:
            if Room.objects.filter(name=class_id).exists():
                return render(request, 'class_room/student_class_room.html', {'people': peoples, "detail": detials, 'books': books, 'recent_books': books[::-1][0:4]})
            else:
                new_room = Room.objects.create(name=class_id)
                new_room.save()
                return render(request, 'class_room/student_class_room.html', {'people': peoples, "detail": detials, 'books': books, 'recent_books': books[::-1][0:4]})


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
        print("It's Student Login......")
        classes = []
        classes_img = []
        try:
            enroll_classes = class_enrolled.objects.filter(
                mail_id=get_user_mail(request))
            print(get_user_mail(request),
                  "this is only passed now............\n\n\n\n\n\n\n\n")
        except:
            enroll_classes = class_enrolled.objects.filter(
                mail_id=request.user.username)

        def get_emails_for_class(class_id):
            # get all instances of the class_enrolled model with the given class_id
            class_enrollments = class_enrolled.objects.filter(
                class_id=class_id)
            # create a list to hold the email IDs
            emails = []
            # iterate over the class_enrollments and add each mail_id to the emails list
            for enrollment in class_enrollments:
                emails.append(enrollment.mail_id)
            # return the list of email IDs
            return emails

        for i in enroll_classes:
            classrooms = ClassRooms.objects.filter(subject_code=i.subject_code)
            for i in classrooms:
                classes.append(i)
                if i.department not in dep:
                    dep.append(i.department)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> get images >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        class_es = []
        for i in classes:
            class_enrollments = class_enrolled.objects.get(
                class_id=i.id)
            class_es.append(class_enrollments)

        img = []
        peoples = []
        temp = []
        for j, i in enumerate(class_es):
            peoples.append(temp)
            temp = []
            print("sub : ", i.subject_code)
            people = class_enrolled.objects.filter(
                subject_code=i.subject_code)
            print('people : ', peoples)
            for i in people:
                person_obj = User.objects.get(id=i.user_id)
                try:
                    obj = Student.objects.get(user=person_obj)
                    temp.append(obj)
                except Exception as e:
                    print(e)
        peoples.append(temp)
        peoples.pop(0)
        temp_people = []
        # ------------------------------------------ to manage the 4 peoples -----------------------------
        for i, j in enumerate(peoples):
            if len(j) >= 4:
                temp_people.append(j)
            else:
                temp_people.append(j[0:4])
        peoples = temp_people
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        obj = User.objects.get(id=request.user.id)
        student_data = Student.objects.get(user=obj)
        try:
            return render(request, 'class_room/student_classroom.html', {'student_data': student_data, 'classes': [[i, j] for i, j in zip(classes, peoples)], 'img': img, 'sem_': sem, 'dep': dep, "user_name": get_user_name(request), "User_role": get_user_role(request), "usr_img": get_user_obj(request)})
        except:
            return render(request, 'class_room/student_classroom.html', {'student_data': student_data, 'classes': [[i, j] for i, j in zip(classes, peoples)], 'img': img, 'sem_': sem, 'dep': dep, "user_name": request.user.username})

    elif is_teacher(request.user):
        obj = User.objects.get(id=request.user.id)
        teacher_data = Teacher.objects.get(user=obj)
        teacher_data_1 = Faculty_details.objects.get(user_name=obj.username)
        get_role = Users.objects.get(user_name=obj.username)
        accountapproval = TMODEL.Teacher.objects.all().filter(
            user_id=request.user.id, status=True)
        if accountapproval:
            print(teacher_data.department)
            classrooms = ClassRooms.objects.filter(
                department=teacher_data.department)
            print(classrooms)
            print(get_role.role, type(get_role.role))
            try:
                if get_role.role == 2:
                    return render(request, 'class_room/staff_classroom.html', {'detail': teacher_data_1, 'teacher_data': teacher_data, 'classes': classrooms, 'img': img, 'sem_': sem, 'dep': dep, "user_name": get_user_name(request), "User_role": get_user_role(request), "usr_img": get_user_obj(request)})
                if get_role.role == 3:
                    return render(request, 'class_room/staff_classroom.html', {'detail': teacher_data_1, 'teacher_data': teacher_data, 'classes': classes, 'img': img, 'sem_': sem, 'dep': dep, "user_name": get_user_name(request), "User_role": get_user_role(request), "usr_img": get_user_obj(request)})
                if get_role.role == 1:
                    return render(request, 'class_room/staff_classroom.html', {'detail': teacher_data_1, 'teacher_data': teacher_data, 'classes': classes, 'img': img, 'sem_': sem, 'dep': dep, "user_name": get_user_name(request), "User_role": get_user_role(request), "usr_img": get_user_obj(request)})
            except:
                if get_role.role == 2:
                    return render(request, 'class_room/staff_classroom.html', {'teacher_data': teacher_data, 'classes': classrooms, 'img': img, 'sem_': sem, 'dep': dep, "user_name": request.user.username})
                if get_role.role == 3:
                    return render(request, 'class_room/staff_classroom.html', {'teacher_data': teacher_data, 'classes': classes, 'img': img, 'sem_': sem, 'dep': dep, "user_name": request.user.username})
        else:
            return render(request, 'teacher/teacher_wait_for_approval.html')
    else:
       if get_role.role == 1:
            return render(request, 'class_room/staff_classroom.html', {'teacher_data': teacher_data, 'classes': classes, 'img': img, 'sem_': sem, 'dep': dep, "user_name": request.user.username})


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
    enroll_class = class_enrolled(
        user_id=request.user.id, mail_id=request.user.username, subject_code=subject_code, class_id=class_id.id)
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


def add_test_marks(request, class_id):
    if request.method == 'POST':
        for i in range(int(request.POST.get('num_rows'))):
            class_id = request.POST.get('class_id_' + str(i))
            ass_no = request.POST.get('ass_no_' + str(i))
            roll_no = request.POST.get('roll_no_' + str(i))
            subject = request.POST.get('subject_' + str(i))
            mark = request.POST.get('mark_' + str(i))
            date = request.POST.get('date_' + str(i))
            daily_test = Internal_test_mark(
                class_id=class_id, assesment_no=ass_no, roll_no=roll_no, subject=subject, mark=mark, Date=date)
            daily_test.save()
        print(class_id)
        return redirect('test_marks', class_id=request.POST.get('class_id_'+str(0)))

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
    sub = Course.objects.all()
    print("sub", sub)
    return render(request, 'class_room/add_test_marks.html', {'class_id': class_id, 'subjects': sub, 'comp': [[i, j] for i, j in enumerate(peoples)]})


def test_marks(request, class_id):
    if request.method == 'POST':
        pass
    peoples = []
    people = class_enrolled.objects.filter(subject_code=class_id)
    for i in people:
        person_obj = User.objects.get(id=i.user_id)
        try:
            obj = Student.objects.get(user=person_obj.id)
            peoples.append(obj)
        except:
            pass
    test_marks = Internal_test_mark.objects.filter(class_id=class_id)
    return render(request, 'class_room/test_marks.html', {'class_id': class_id, 'test_marks': [[i, j, Student.objects.filter(role_no=j.roll_no)[0].get_name] for i, j in enumerate(test_marks)], 'students': peoples})


def edit_test_marks(request, class_id, sub, ass_no):
    if request.method == 'POST':
        for i in range(int(request.POST.get('num_rows'))):
            test = Internal_test_mark.objects.get(
                id=request.POST.get('test_id_' + str(i)))
            class_id = request.POST.get('class_id_' + str(i))
            ass_no = request.POST.get('ass_no_' + str(i))
            roll_no = request.POST.get('roll_no_' + str(i))
            subject = request.POST.get('subject_' + str(i))
            mark = request.POST.get('mark_' + str(i))
            date = request.POST.get('date_' + str(i))
            test.class_id = class_id
            test.assesment_no = ass_no
            test.roll_no = roll_no
            test.subject = subject
            test.mark = mark
            test.Date = date
            test.save()
        print(class_id)
        return redirect('test_marks', class_id=request.POST.get('class_id_'+str(0)))

    test = Internal_test_mark.objects.filter(
        class_id=class_id, subject=sub, assesment_no=ass_no)
    sub = Course.objects.all()

    return render(request, 'class_room/edit_test_mark.html', {'subjects': sub, 'class_id': class_id, 'comp': [[i, j] for i, j in enumerate(test)]})


def marks_by_class(request, class_id):
    # retrieve all Sec_Daily_test_mark objects for the specified class
    marks = Sec_Daily_test_mark.objects.filter(class_id=class_id)

    # create a nested dictionary to store the marks by user and subject
    class_data = {}
    for mark in marks:
        user = mark.user_name
        subject = mark.subject
        if user and subject and mark.mark is not None:
            if user not in class_data:
                class_data[user] = {}
            if subject not in class_data[user]:
                class_data[user][subject] = []
            class_data[user][subject].append(mark)

    # pass the data to the template
    context = {'class_id': class_id, 'class_data': class_data}
    return render(request, 'class_room/daily_mark.html', context)


def user_marks(request, user_name):
    user_marks = Sec_Daily_test_mark.objects.filter(
        user_name=user_name).order_by('Date')
    user_subjects = set([mark.subject for mark in user_marks])
    context = {'user_marks': user_marks, 'user_subjects': user_subjects}
    return render(request, 'user_marks.html', context)


def show_actions(request, class_id):
    cls_obj = ClassRooms.objects.get(subject_code=class_id)

    return render(request, "class_room/action_options.html", {'class_obj': cls_obj})


def mark_option(request, class_id):
    cls_obj = ClassRooms.objects.get(subject_code=class_id)
    return render(request, "class_room/mark_option.html", {'class_obj': cls_obj})


def attendes_option(request, class_id):
    cls_obj = ClassRooms.objects.get(subject_code=class_id)
    return render(request, "class_room/attendes_actions.html", {'class_obj': cls_obj})


def Dailytest_marksby_date(request, user_name):
    # Retrieve all marks for the given user
    user_marks = Sec_Daily_test_mark.objects.filter(
        user_name=user_name).order_by('Date')

    # Get all unique dates for the retrieved marks
    dates = user_marks.values_list('Date', flat=True).distinct()

    # Get all unique subjects for the retrieved marks
    subjects = user_marks.values_list('subject', flat=True).distinct()

    # Generate HTML table
    table = '<table><thead><tr><th>Subject</th>'
    for date in dates:
        table += f'<th>{date}</th>'
    table += '</tr></thead><tbody>'
    for subject in subjects:
        table += f'<tr><td>{subject}</td>'
        for date in dates:
            try:
                mark = user_marks.get(subject=subject, Date=date).mark
                table += f'<td>{mark}</td>'
            except Sec_Daily_test_mark.DoesNotExist:
                table += '<td></td>'
        table += '</tr>'
    table += '</tbody></table>'

    context = {'marks_table': table}
    # return render(request, 'user_marks.html', context)
    return render(request, 'class_room/Dailytest_marksby_date.html', context)


def list_user_for_mark(request, class_id):
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
    return render(request, 'class_room/list_user_for_mark.html', {'people': peoples})


def user_mark_view(request, class_id):
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
    if request.method == 'POST':
        user_name = request.POST['user_name']
        date = request.POST['date']
        department = request.POST['department']
        if department == '':
            marks = Sec_Daily_test_mark.objects.filter(
                user_name=user_name, Date=date)
        else:
            marks = Sec_Daily_test_mark.objects.filter(
                user_name=user_name, Date=date, subject=department)
        context = {'marks': marks}
        return render(request, 'class_room/user_marks.html', context)
    return render(request, 'class_room/user_mark_form.html', {'people': peoples})


def get_internal_test_marks(request):
    marks = None
    class_id = ''
    assesment_no = ''
    date_str = ''

    if request.method == 'GET':
        class_id = request.GET.get('class_id')
        assesment_no = request.GET.get('assesment_no')
        date_str = request.GET.get('date')

        if class_id and assesment_no:
            marks = Internal_test_mark.objects.filter(
                class_id=class_id, assesment_no=assesment_no)

            if date_str:
                # Parse the date string to get the year
                date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                year = date.year

                # Filter marks based on year
                marks = marks.filter(Date__year=year)

    context = {
        'marks': marks,
        'class_id': class_id,
        'assesment_no': assesment_no,
        'date': date_str,
    }

    return render(request, 'class_room/internal_test_marks.html', context)


def Dailystudenttest_marksby_date(request, user_name):
    # Retrieve all marks for the given user
    user_marks = Sec_Daily_test_mark.objects.filter(
        user_name=user_name).order_by('Date')

    # Get all unique dates for the retrieved marks
    dates = user_marks.values_list('Date', flat=True).distinct()

    # Get all unique subjects for the retrieved marks
    subjects = user_marks.values_list('subject', flat=True).distinct()

    # Generate HTML table
    table = '<table><thead><tr><th>Subject</th>'
    for date in dates:
        table += f'<th>{date}</th>'
    table += '</tr></thead><tbody>'
    for subject in subjects:
        table += f'<tr><td>{subject}</td>'
        for date in dates:
            try:
                mark = user_marks.get(subject=subject, Date=date).mark
                table += f'<td>{mark}</td>'
            except Sec_Daily_test_mark.DoesNotExist:
                table += '<td></td>'
        table += '</tr>'
    table += '</tbody></table>'

    context = {'marks_table': table}
    # return render(request, 'user_marks.html', context)
    return render(request, 'class_room/Dailystudenttest_marksby_date.html', context)


def ToDoList(request):
    return render(request, "ToDoList/index.html", student_detials(request, 'ToDo-List'))


def staffToDoList(request):
    return render(request, "ToDoList/staff_index.html", staff_detials(request, 'ToDo-List'))


def student_mark_option(request, class_id):
    cls_obj = ClassRooms.objects.get(subject_code=class_id)
    return render(request, "class_room/student_mark_option.html", student_detials(request, 'Mark Options', {'class_obj': cls_obj}))


def student_get_mark(request, user_name):
    # Retrieve all marks for the given user
    user_marks = Sec_Daily_test_mark.objects.filter(
        user_name=user_name).order_by('Date')

    # Get all unique dates for the retrieved marks
    dates = user_marks.values_list('Date', flat=True).distinct()

    # Get all unique subjects for the retrieved marks
    subjects = user_marks.values_list('subject', flat=True).distinct()

    # Generate HTML table
    table = '<table><thead><tr><th>Subject</th>'
    for date in dates:
        table += f'<th>{date}</th>'
    table += '</tr></thead><tbody>'
    for subject in subjects:
        table += f'<tr><td>{subject}</td>'
        for date in dates:
            try:
                mark = user_marks.get(subject=subject, Date=date).mark
                table += f'<td>{mark}</td>'
            except Sec_Daily_test_mark.DoesNotExist:
                table += '<td></td>'
        table += '</tr>'
    table += '</tbody></table>'

    context = {'marks_table': table}
    # return render(request, 'user_marks.html', context)
    return render(request, 'class_room/get_test__mark.html', context)


def student_int_test_marks(request, roll_no):
    queryset = Internal_test_mark.objects.filter(
        roll_no=roll_no
    ).order_by('-assesment_no', '-Date')

    year = request.GET.get('year')
    if year:
        start_date = datetime.strptime(f"{year}-01-01", "%Y-%m-%d").date()
        end_date = datetime.strptime(f"{year}-12-31", "%Y-%m-%d").date()

        queryset = queryset.filter(
            Date__range=(start_date, end_date)
        )

    context = {
        'roll_no': roll_no,
        'queryset': queryset
    }

    return render(request, 'class_room/internal_test_mark_by_user.html', student_detials(request, 'Internal Test Mark', context))


import json
from datetime import date

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)


import json
from datetime import date

def view_attendees_by_roolno(request, roll_no):
    attendees = Attendees.objects.filter(roll_no=roll_no).order_by('-Date')

    attendees_list = []
    for attendee in attendees:
        attendee_dict = {
            'Date': attendee.Date,
            'subject_states': attendee.subject_states
        }
        attendees_list.append(attendee_dict)

    context = {
        'roll_no': roll_no,
        'attendees':attendees,
        'attendeesj': json.dumps(attendees_list, cls=CustomJSONEncoder),
    }
    return render(request, 'class_room/view_attendeesbyroolno.html', student_detials(request, 'View Attendence', context))


def search_view(request):
    if request.method == 'GET':
        query = request.GET.get('google_search')
        if query:
            query = urllib.parse.quote(query)
            results = []
            for url in search(query, num_results=50):
                # process the search results
                results.append(url)
            return render(request, 'class_room/search_results.html', {'results': results, 'query': query})
    return render(request, 'class_room/search_results.html')
