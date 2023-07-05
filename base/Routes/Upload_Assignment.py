from django.shortcuts import render, get_object_or_404, redirect
from base.models import Upload_Assignment

def upload_assignment_list(request):
    assignments = Upload_Assignment.objects.all()
    return render(request, 'assignment/upload_assignment_list.html', {'assignments': assignments})

def upload_assignment_create(request,qst_id):
    if request.method == 'POST':
        file = request.FILES['file']
        upload_assignment = Upload_Assignment.objects.create(update_by=request.user.id, File=file, Assignment_id=qst_id)
        upload_assignment.save()
        return redirect('upload_assignment_list')
    return render(request, 'assignment/upload_assignment_create.html')

def upload_assignment_edit(request, pk):
    upload_assignment = get_object_or_404(Upload_Assignment, pk=pk)
    if request.method == 'POST':
        update_by = request.POST.get('update_by')
        file = request.FILES.get('file')
        assignment_id = request.POST.get('assignment_id')
        upload_assignment.update_by = update_by
        if file:
            upload_assignment.File = file
        upload_assignment.Assignment_id = assignment_id
        upload_assignment.save()
        return redirect('upload_assignment_list')
    return render(request, 'assignment/upload_assignment_edit.html', {'upload_assignment': upload_assignment})

def upload_assignment_delete(request, pk):
    upload_assignment = get_object_or_404(Upload_Assignment, pk=pk)
    if request.method == 'POST':
        upload_assignment.delete()
        return redirect('upload_assignment_list')
    return render(request, 'assignment/upload_assignment_delete.html', {'upload_assignment': upload_assignment})
