from django.shortcuts import render, get_object_or_404, redirect
from base.models import Assignment
from .Tool.Tools import student_detials, staff_detials
<<<<<<< HEAD


def assignment_list(request,class_id):
    assignments = Assignment.objects.filter(class_id=class_id)
    return render(request, 'assignment/assignment_list.html',staff_detials(request,'assignment list',{'assignments': assignments,'class_id':class_id}))
=======

def assignment_list(request,class_id):
    assignments = Assignment.objects.filter(class_id=class_id)
    return render(request, 'assignment/assignment_list.html', staff_detials(request,'List Assignment',{'assignments': assignments,'class_id':class_id}))
>>>>>>> 03b413a6eca33bae4c2ae75ab9c552ea9a04ddc0

def assignment_add(request,class_id):
    if request.method == 'POST':
        subject = request.POST['subject']
        title = request.POST['title']
        details = request.POST['details']
        assignment = Assignment(update_by=request.user.id, subject=subject, title=title, details=details,class_id=class_id)
        assignment.save()
        return redirect('assignment_list',class_id=class_id)
    return render(request, 'assignment/assignment_add.html',student_detials(request,'Add Assignment'))

def assignment_edit(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        assignment.subject = request.POST['subject']
        assignment.title = request.POST['title']
        assignment.details = request.POST['details']
        assignment.save()
        return redirect('assignment_list')
<<<<<<< HEAD
    return render(request, 'assignment/assignment_edit.html',staff_detials(request,' Edit Assignment',{'assignment': assignment}) )
=======
    return render(request, 'assignment/assignment_edit.html', staff_detials(request,'Edit Assignment',{'assignment': assignment}))
>>>>>>> 03b413a6eca33bae4c2ae75ab9c552ea9a04ddc0

def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        assignment.delete()
        return redirect('assignment_list')
    return render(request, 'assignment/assignment_delete.html', staff_detials(request,'Edit Delete',{'assignment': assignment}))
