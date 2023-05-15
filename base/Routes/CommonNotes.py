from django.shortcuts import render, get_object_or_404, redirect
from ..models import Note, EbookForClass, Department
from .Tool.Tools import student_detials, staff_detials


def note_by_class(request, class_id):
    books = EbookForClass.objects.filter(Class_id=class_id)
    collections = []
    course = []
    for i in books:
        course.append(i.course)
    for j in list(set(course)):
        collections.append(EbookForClass.objects.filter(course=j))
    return render(request, 'commonNotes/student_class_note_list.html', student_detials(request, 'Common Notes', {'note_lis': collections}))


def note_by_class_staff(request, class_id):
    books = EbookForClass.objects.filter(Class_id=class_id)
    collections = []
    course = []
    for i in books:
        course.append(i.course)
    for j in list(set(course)):
        collections.append(EbookForClass.objects.filter(course=j))
    return render(request, 'commonNotes/staff_class_note_list.html', staff_detials(request, 'Common Notes', {'note_lis': collections}))


def notes_list(request):
    notes = Note.objects.all()
    dep = set()
    note_lis = []
    for i in notes:
        dep.update(i.department)
    print(dep)
    for j in list(dep):
        obj = Note.objects.filter(department=j)
        note_lis.append(obj)
    return render(request, 'commonNotes/notes_list.html', staff_detials(request,'Notes List',{'notes': notes, 'note_lis': note_lis}))
    

def student_notes_list(request):
    notes = Note.objects.all()
    dep = []
    note_lis = []
    for i in notes:
        dep.append(i.department)
    for j in list(set(dep)):
        obj = Note.objects.filter(department=j)
        note_lis.append(obj)
    return render(request, 'commonNotes/student_note_list.html', student_detials(request, 'Common Notes', {'notes': notes, 'note_lis': note_lis}))


def staff_notes_list(request):
    notes = Note.objects.all()
    return render(request, 'commonNotes/staff_note_list.html', staff_detials(request, 'Common Notes', {'notes': notes}))


def common_notes_list(request):
    notes = Note.objects.all()
    return render(request, 'commonNotes/Common_notes.html', {'notes': notes})


def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return render(request, 'commonNotes/note_detail.html', {'note': note})


def create_note(request):
    if request.method == 'POST':
        department = request.POST.get('department')
        semester = request.POST.get('semester')
        notes_title = request.POST.get('notes_title')
        regulation = request.POST.get('regulation')
        subcode = request.POST.get('subcode')
        cover_image = request.POST.get('cover_image')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        note = Note(department=department, semester=semester, notes_title=notes_title, regulation=regulation,
                    subcode=subcode, description=description, file=file, cover_image=cover_image)
        note.save()
        return redirect('notes_list')
    return render(request, 'commonNotes/note_form.html',staff_detials(request,'Upload Notes',{'dep':Department.objects.all()}))

def update_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        department = request.POST.get('department')
        semester = request.POST.get('semester')
        notes_title = request.POST.get('notes_title')
        regulation = request.POST.get('regulation')
        subcode = request.POST.get('subcode')
        cover_image = request.POST.get('cover_image')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        note.department = department
        note.semester = semester
        note.cover_image = cover_image
        note.notes_title = notes_title
        note.regulation = regulation
        note.subcode = subcode
        note.description = description
        if file:
            note.file = file
        note.save()
        return redirect('note_detail', note_id=note.id)
    return render(request, 'commonNotes/note_form.html', {'note': note})


def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.delete()
    return redirect('notes_list')
