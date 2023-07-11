from django.shortcuts import render, get_object_or_404, redirect
from base.models import Upload_Assignment, Assignment,Student, Assignment_mark
from .Tool.Tools import student_detials, staff_detials
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

def upload_assignment_list(request,id):
    users = Upload_Assignment.objects.filter(Assignment_id=id).values('update_by').distinct()
    sample=[]
    for i in users:
        print("id is....",i.get('update_by'))
        user = User.objects.get(id=i.get('update_by'))
        student = Student.objects.get(user=user)
        sample.append(student)
    print(sample)
    return render(request, 'teacher/assignments.html', staff_detials(request,'Submited Students',{'datas': zip(users,sample)}))
 
def assignment_mark(request,id,a_id,class_id,student_id):
    mark = request.POST.get('mark')
    exists = Assignment_mark.objects.filter(Assignment_id=id).exists()
    print("mark is  : ",mark,student_id)
    if not exists: 
       new_assignment_mark = Assignment_mark(
            student_id=student_id,  # Set the student_id value
            Assignment_id=id,  # Set the Assignment_id value
            mark=90  # Set the mark value
        )
    else:
       return render(request,'attandees/mark_already_updated.html')
    new_assignment_mark.save()
    return redirect('upload_assignment_list1',id=id,a_id=a_id,class_id=class_id)

def edit_assignment_mark(request,id,a_id,class_id,student_id):
    mark = request.POST.get("mark")
    try:
        assignment_mark = Assignment_mark.objects.get(id=id)
        assignment_mark.mark = mark
        assignment_mark.save()
        return redirect('upload_assignment_list1',id=student_id,a_id=a_id,class_id=class_id)
    except Assignment_mark.DoesNotExist:
        return None

def upload_assignment_list1(request,id,a_id,class_id):
    users = Upload_Assignment.objects.filter(Assignment_id=id).values('update_by','Assignment_id').distinct()
    sample=[]
    usr = []
    for i in users:
        user = User.objects.get(id=i.get('update_by'))
        student = Student.objects.get(user=user)
        sample.append(student)
        usr.append(Upload_Assignment.objects.filter(Assignment_id=i.get('update_by')))
    first_user = users.first()
    try:
        first_update_by = first_user['Assignment_id']
    except:
        return render(request,'msg/no_one_updated.html')
    print(first_update_by,sample)
    title = Assignment.objects.get(id=first_update_by)
    return render(request, 'teacher/assignments.html', staff_detials(request,'Submited Students',{'datas': zip(users,sample),'status':a_id,"class_id":class_id,'id':id,'title':title,'asm_id':first_update_by}))


def staff_upload_assignment_create(request,qst_id,state,class_id,std):
    print("std",std)
    try:
        file = Upload_Assignment.objects.filter(update_by=std)  # Add appropriate filter conditions if needed
    except Upload_Assignment.DoesNotExist:
        file = None
        
    obj1 = Assignment.objects.filter(id=qst_id)
    obj = Assignment.objects.get(id=qst_id)
    for i in obj1:
        print(i.update_by)
    print(std,qst_id)
    try:
        assignment_mark = Assignment_mark.objects.get(student_id=std, Assignment_id=qst_id)
        mark = assignment_mark
    except ObjectDoesNotExist:
        mark = None
    
    return render(request, 'assignment/staff_upload_assignment_create.html',staff_detials(request,'view Assignment',{'data':obj,"file":file,"qst_id":qst_id,"state":state,"class_id":class_id,"std":std,"mark":mark}))


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> student assiment >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def upload_assignment_create(request,qst_id):
    obj = Assignment.objects.get(id=qst_id)
    try:
        file = Upload_Assignment.objects.filter(update_by=request.user.id)  # Add appropriate filter conditions if needed
    except Upload_Assignment.DoesNotExist:
        file = None
    try:
        assignment_mark = Assignment_mark.objects.get(student_id=request.user.id, Assignment_id=qst_id)
        mark = assignment_mark
    except ObjectDoesNotExist:
        mark = None
    if request.method == 'POST':
        file = request.FILES['file']
        upload_assignment = Upload_Assignment.objects.create(update_by=request.user.id, File=file, Assignment_id=qst_id)
        upload_assignment.save()
        return redirect('upload_assignment_create',qst_id=qst_id)
    return render(request, 'assignment/upload_assignment_create.html',student_detials(request,"upload Assignment",{'data':obj,"file":file,"qst_id":qst_id,"mark":mark}))
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
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
    return render(request, 'assignment/upload_assignment_delete.html',student_detials(request,"Delete_assignment", {'upload_assignment': upload_assignment,"qst_id":qst_id}))
