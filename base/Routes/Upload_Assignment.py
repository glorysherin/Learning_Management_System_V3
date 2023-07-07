from django.shortcuts import render, get_object_or_404, redirect
from base.models import Upload_Assignment, Assignment,Student, Users
from .Tool.Tools import student_detials, staff_detials
from django.contrib.auth.models import User

def upload_assignment_list(request,id):
    users = Upload_Assignment.objects.filter(Assignment_id=id).values('update_by')
    sample=[]
    for i in users:
        print("id is....",i.get('update_by'))
        user = User.objects.get(id=i.get('update_by'))
        student = Student.objects.get(user=user)
        sample.append(student)
    print(sample)
    return render(request, 'teacher/assignments.html', staff_detials(request,'Submited Students',{'datas': zip(users,sample)}))


def upload_assignment_create(request,qst_id):
    obj = Assignment.objects.get(id=qst_id)
    try:
        file = Upload_Assignment.objects.filter()  # Add appropriate filter conditions if needed
    except Upload_Assignment.DoesNotExist:
        file = None
    if request.method == 'POST':
        file = request.FILES['file']
        upload_assignment = Upload_Assignment.objects.create(update_by=request.user.id, File=file, Assignment_id=qst_id)
        upload_assignment.save()
        return redirect('upload_assignment_create',qst_id=qst_id)
    return render(request, 'assignment/upload_assignment_create.html',{'data':obj,"file":file,"qst_id":qst_id})

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

def upload_assignment_delete(request, pk, qst_id):
    upload_assignment = get_object_or_404(Upload_Assignment, pk=pk)
    if request.method == 'POST':
        upload_assignment.delete()
        return redirect('upload_assignment_create',qst_id=qst_id)
    return render(request, 'assignment/upload_assignment_delete.html', {'upload_assignment': upload_assignment,"qst_id":qst_id})
