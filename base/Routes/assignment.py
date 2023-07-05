from django.shortcuts import render, get_object_or_404, redirect
from base.models import Assignment

def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, 'assignment/assignment_list.html', {'assignments': assignments})

def assignment_add(request,class_id):
    if request.method == 'POST':
        subject = request.POST['subject']
        title = request.POST['title']
        details = request.POST['details']
        assignment = Assignment(update_by=request.user.id, subject=subject, title=title, details=details,class_id=class_id)
        assignment.save()
        return redirect('assignment_list')
    return render(request, 'assignment/assignment_add.html')

def assignment_edit(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        assignment.subject = request.POST['subject']
        assignment.title = request.POST['title']
        assignment.details = request.POST['details']
        assignment.save()
        return redirect('assignment_list')
    return render(request, 'assignment/assignment_edit.html', {'assignment': assignment})

def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        assignment.delete()
        return redirect('assignment_list')
    return render(request, 'assignment/assignment_delete.html', {'assignment': assignment})
