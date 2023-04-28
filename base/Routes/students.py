from django.shortcuts import render, get_object_or_404, redirect
from base import models
from .Forms import student_forms
from ..models import Users, Student, Faculty_details, Sec_Daily_test_mark
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from base import models as QMODEL
from django.contrib.auth.models import User
# for showing signup/login button for student
from .Tool.Tools import student_detials, staff_detials

# views.py


def students_list(request):
    students = Student.objects.all()
    departments = set([student.department for student in students])
    context = {
        'students': students,
        'departments': departments,
    }
    return render(request, 'student/students_list.html', context)


def admin_students_list(request):
    students = Student.objects.all()
    departments = set([student.department for student in students])
    context = {
        'students': students,
        'departments': departments,
    }
    return render(request, 'student/admin_students_list.html', context)


def students_list_by_dep(request):
    usr_id = request.user.id
    usr_obj = User.objects.get(id=usr_id)
    name = Users.objects.get(user_name=usr_obj.username)
    faculty_details = Faculty_details.objects.get(user_name=name.user_name)
    students = Student.objects.filter(department=faculty_details.department)
    departments = set([student.department for student in students])
    context = {
        'students': students,
        'departments': departments,
    }
    return render(request, 'student/students_list.html',  staff_detials(request, 'Manage Students',context))


def student_profile(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    usr_id = request.user.id
    usr_obj = User.objects.get(id=usr_id)
    std_data = Student.objects.get(user=usr_obj)
    dict = {
        'usr': std_data,
        'page': 'Student Profile',
        'student': student
    }
    return render(request, 'student/student_profile.html', dict)


def student_delete(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    students = Student.objects.all()
    departments = set([student.department for student in students])
    context = {
        'students': students,
        'departments': departments,
        'student': student
    }
    return render(request, 'student/students_list.html', context)


def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.user.first_name = request.POST['first_name']
        student.user.last_name = request.POST['last_name']
        student.mail_id = request.POST['email']
        student.address = request.POST['address']
        student.mobile = request.POST['mobile']
        student.joinned_year = request.POST['joinned_year']
        student.role_no = request.POST['role_no']
        student.department = request.POST['department']
        student.profile_pic = request.FILES['file_']
        student.user.save()
        student.save()
        return redirect('students_list')
    else:
        context = {'student': student}
        return render(request, 'student/edit_student_profile.html', student_detials(request, 'Edit Detials', context))


def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'student/studentclick.html')


def student_signup_view(request):
    userForm = student_forms.StudentUserForm()
    studentForm = student_forms.StudentForm()
    mydict = {'userForm': userForm, 'studentForm': studentForm}
    if request.method == 'POST':
        userForm = student_forms.StudentUserForm(request.POST)
        studentForm = student_forms.StudentForm(request.POST, request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            student = studentForm.save(commit=False)
            student.user = user
            student.save()
            add_user = Users(user_name=user.username,
                             mail_id=user.username, password=user.password, role='4')
            add_user.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request, 'student/studentsignup.html', context=mydict)


def add_student_signup_view(request):
    userForm = student_forms.StudentUserForm()
    studentForm = student_forms.StudentForm()
    mydict = {'userForm': userForm, 'studentForm': studentForm}
    if request.method == 'POST':
        userForm = student_forms.StudentUserForm(request.POST)
        studentForm = student_forms.StudentForm(request.POST, request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            student = studentForm.save(commit=False)
            student.user = user
            student.save()
            add_user = Users(user_name=user.username,
                             mail_id=user.username, password=user.password, role='4')
            add_user.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('addstudentlogin')
    return render(request, 'student/studentsignup.html', staff_detials(request,'Add Student',mydict))


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):

    usr_id = request.user.id
    usr_obj = User.objects.get(id=usr_id)
    std_data = Student.objects.get(user=usr_obj)
    data = Sec_Daily_test_mark.objects.filter(
        user_name=Student.get_name).order_by('Date')
    for i in data:
        print(i.class_id, i.user_name)
    dict = {
        'datas': data,
        'total_course': QMODEL.Course.objects.all().count(),
        'total_question': QMODEL.Question.objects.all().count(),
        'usr': std_data,
        'page': 'Dashboard'
    }

    return render(request, 'student/student_dashboard.html', context=dict)


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'student/student_exam.html', student_detials(request, 'Examination', {'courses': courses}))


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    total_questions = QMODEL.Question.objects.all().filter(course=course).count()
    questions = QMODEL.Question.objects.all().filter(course=course)
    total_marks = 0
    for q in questions:
        total_marks = total_marks + q.marks

    return render(request, 'student/take_exam.html', student_detials(request, 'Take Exam', {'course': course, 'total_questions': total_questions, 'total_marks': total_marks}))


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    questions = QMODEL.Question.objects.all().filter(course=course)
    if request.method == 'POST':
        pass
    response = render(request, 'student/start_exam.html', student_detials(request,
                      'start-exam', {'course': course, 'questions': questions}))
    response.set_cookie('course_id', course.id)
    return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course = QMODEL.Course.objects.get(id=course_id)

        total_marks = 0
        questions = QMODEL.Question.objects.all().filter(course=course)
        for i in range(len(questions)):

            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks = total_marks
        result.exam = course
        result.student = student
        result.save()

        return HttpResponseRedirect('view-result')


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'student/view_result.html', {'courses': courses})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request, pk):
    course = QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results = QMODEL.Result.objects.all().filter(
        exam=course).filter(student=student)
    return render(request, 'student/check_marks.html', {'results': results})


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'student/student_marks.html', student_detials(request, 'My Marks', {'courses': courses}))
