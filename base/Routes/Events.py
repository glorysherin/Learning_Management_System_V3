# views.py
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, redirect
from ..models import Event


def event_list(request):
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'Events/event_list.html', context)


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    context = {'event': event}
    return render(request, 'Events/event_detail.html', context)


def event_create(request):
    if request.method == 'POST':
        date = request.POST['date']
        event_name = request.POST['event_name']
        event_photo = request.POST['event_photo']
        event_description = request.POST['event_description']
        poster_link = request.POST['poster_link']
        event = Event.objects.create(date=date, event_name=event_name, event_photo=event_photo,
                                     event_description=event_description, poster_link=poster_link)
        return redirect('event_detail', event_id=event.pk)
    return render(request, 'Events/event_form.html')


def event_edit(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        event.date = request.POST['date']
        event.event_name = request.POST['event_name']
        event.event_photo = request.POST['event_photo']
        event.event_description = request.POST['event_description']
        event.poster_link = request.POST['poster_link']
        event.save()
        return redirect('event_detail', event_id=event.pk)
    context = {'event': event}
    return render(request, 'Events/event_form.html', context)


def event_delete(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.delete()
    return redirect('event_list')


def event_add(request):
    if request.method == 'POST':
        date = request.POST['date']
        event_name = request.POST['event_name']
        event_photo = request.POST['event_photo']
        event_description = request.POST['event_description']
        poster_link = request.POST['poster_link']

        event = Event.objects.create(
            date=date,
            event_name=event_name,
            event_photo=event_photo,
            event_description=event_description,
            poster_link=poster_link
        )
        return redirect('event_list')

    return render(request, 'Events/event_add.html')
