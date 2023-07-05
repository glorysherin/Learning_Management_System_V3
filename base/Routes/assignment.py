from django.shortcuts import render, get_object_or_404, redirect
from base.models import Assignment

def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, 'assignments/assignment_list.html', {'assignments': assignments})

def assignment_add(request):
    if request.method == 'POST':
        update_by = request.POST['update_by']
        subject = request.POST['subject']
        title = request.POST['title']
        details = request.POST['details']
        file = request.FILES['file']
        assignment = Assignment(update_by=update_by, subject=subject, title=title, details=details, file=file)
        assignment.save()
        return redirect('assignments:assignment_list')
    return render(request, 'assignments/assignment_add.html')

def assignment_edit(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        assignment.update_by = request.POST['update_by']
        assignment.subject = request.POST['subject']
        assignment.title = request.POST['title']
        assignment.details = request.POST['details']
        if 'file' in request.FILES:
            assignment.file = request.FILES['file']
        assignment.save()
        return redirect('assignments:assignment_list')
    return render(request, 'assignments/assignment_edit.html', {'assignment': assignment})

def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        assignment.delete()
        return redirect('assignments:assignment_list')
    return render(request, 'assignments/assignment_delete.html', {'assignment': assignment})
