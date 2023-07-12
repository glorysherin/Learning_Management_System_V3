from django.shortcuts import render, redirect, get_object_or_404
from ..models import NoteCourse, Ebook
from .Forms.Notes_form import EbookForm, CourseForm
from .Tool.Tools import student_detials, staff_detials

def course_list(request):
    courses = NoteCourse.objects.all()
    return render(request, 'notes/course_list.html', staff_detials(request,'Course List',{'courses': courses}))

def course_detail(request, pk):
    course = get_object_or_404(NoteCourse, pk=pk)
    return render(request, 'notes/course_detail.html', staff_detials(request,'Course Detail',{'course': course,'pk':pk}))

def course_add(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    context = {'form': form}
    return render(request, 'notes/course_add.html',staff_detials(request,'Add Course',context))

def course_delete(request, pk):
    NoteCourse.objects.get(id=pk).delete()
    return redirect("course_list")


def course_edit(request, pk):
    course = NoteCourse.objects.get(id=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        semester = request.POST.get('semester')
        course_id = request.POST.get('course_id')

        # Update the course object with the new values
        course.name = name
        course.description = description
        course.semester = semester
        course.course_id = course_id
        course.save()

        return redirect('course_detail', pk=course.pk)
    
    return render(request, 'notes/course_edit.html', staff_detials(request,'Edit Course',{'course': course}))


def course_delete(request, pk):
    course = get_object_or_404(NoteCourse, pk=pk)
    course.delete()
    return redirect('course_list')

def ebook_add(request):
    if request.method == 'POST':
        form = EbookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = EbookForm()
    return render(request, 'notes/ebook_add.html', staff_detials(request,'Add E-Book',{'form': form}))

def ebook_edit(request, pk):
    ebook = get_object_or_404(Ebook, pk=pk)
    if request.method == 'POST':
        form = EbookForm(request.POST, request.FILES, instance=ebook)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = EbookForm(instance=ebook)
    return render(request, 'notes/ebook_edit.html', {'form': form})

def ebook_delete(request, pk):
    ebook = get_object_or_404(Ebook, pk=pk)
    ebook.delete()
    return redirect('course_list')

def book_list(request):
    books = Ebook.objects.all()
    return render(request, 'notes/ebook_list.html', {'books': books})
