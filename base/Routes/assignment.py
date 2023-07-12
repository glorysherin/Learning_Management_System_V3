from django.shortcuts import render, get_object_or_404, redirect
from base.models import Assignment, Teacher
from django.contrib.auth.models import User
from .Tool.Tools import student_detials, staff_detials

def assignment_list(request,class_id):
    assignments = Assignment.objects.filter(class_id=class_id)
    return render(request, 'assignment/assignment_list.html', staff_detials(request,'List Assignment',{'assignments': assignments,'class_id':class_id}))

def assignment_add(request,class_id):
    if request.method == 'POST':
        subject = request.POST['subject']
        title = request.POST['title']
        details = request.POST['details']
        assignment = Assignment(update_by=request.user.id, subject=subject, title=title, details=details,class_id=class_id)
        assignment.save()
        return redirect('assignment_list',class_id=class_id)
    try:
        Teacher.objects.get(user=User.objects.get(id=request.user.id))
        return render(request, 'assignment/assignment_add.html',staff_detials(request,'Add Assignment'))
    except:
        return render(request, 'assignment/assignment_add.html',student_detials(request,'Add Assignment'))

def assignment_edit(request, pk,class_id):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        assignment.subject = request.POST['subject']
        assignment.title = request.POST['title']
        assignment.details = request.POST['details']
        assignment.save()
        return redirect('assignment_list',class_id=class_id)
    return render(request, 'assignment/assignment_edit.html', staff_detials(request,'Edit Assignment',{'assignment': assignment}))

def assignment_delete(request, pk,class_id):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        assignment=Assignment.objects.get(id=pk)
        assignment.delete()
        return redirect('assignment_list',class_id=class_id)
    return render(request, 'assignment/assignment_delete.html', staff_detials(request,'Edit Delete',{'assignment': assignment,'class_id':class_id}))
