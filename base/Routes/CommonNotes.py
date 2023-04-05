from django.shortcuts import render, get_object_or_404, redirect
from ..models import Note


def notes_list(request):
    notes = Note.objects.all()
    return render(request, 'commonNotes/notes_list.html', {'notes': notes})


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
        description = request.POST.get('description')
        file = request.FILES.get('file')
        note = Note(department=department, semester=semester, notes_title=notes_title, regulation=regulation,
                    subcode=subcode, description=description, file=file)
        note.save()
        return redirect('notes_list')
    return render(request, 'commonNotes/note_form.html')


def update_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        department = request.POST.get('department')
        semester = request.POST.get('semester')
        notes_title = request.POST.get('notes_title')
        regulation = request.POST.get('regulation')
        subcode = request.POST.get('subcode')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        note.department = department
        note.semester = semester
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
