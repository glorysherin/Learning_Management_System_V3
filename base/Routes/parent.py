from django.shortcuts import render, get_object_or_404, redirect
from ..models import Attendees, Sec_Daily_test_mark,Internal_test_mark, Student, class_enrolled, ClassRooms
from .Tool.Tools import student_detials, staff_detials
from datetime import datetime
from django.db.models import Sum, Max
from datetime import date
import json

def parent_class_list(request,roll_no):
    try:
        stu_id = Student.objects.get(role_no=roll_no).user.id
    except:
        return render(request,'msg/std_doesn_exist.html')
    classes = class_enrolled.objects.filter(user_id=stu_id)
    room_list = []
    for i in classes:
        room_list.append(ClassRooms.objects.get(subject_code=i.subject_code))
            # return render(request,'parent/parent_home.html',{'role_no':role_no,'std':obj})
        
    return render(request,'parent/class_list.html',{'classes':room_list,'roll_no':roll_no})

def view_data(request,roll_no,class_id):
    obj = Student.objects.get(role_no=roll_no)
    return render(request,'parent/parent_home.html',{'role_no':roll_no,'std':obj,'class_id':class_id}) 

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

def parent_student_int_test_marks(request, roll_no,class_id):
    queryset = Internal_test_mark.objects.filter(
        roll_no=roll_no, class_id=class_id
    ).order_by('-Date').order_by('-assesment_no')

    year = request.GET.get('year')
    if year:
        start_date = datetime.strptime(f"{year}-01-01", "%Y-%m-%d").date()
        end_date = datetime.strptime(f"{year}-12-31", "%Y-%m-%d").date()

        queryset = queryset.filter(
            Date__range=(start_date, end_date)
        )

    context = {
        'roll_no': roll_no,
        'queryset': queryset
    }

    return render(request, 'parent/internal_test_mark_by_user.html', context)


def parentmark_list(request, roll_no, class_id):
    # retrieve all the unique dates for the specified roll number
    dates = Sec_Daily_test_mark.objects.filter(
        roll_no=roll_no, class_id=class_id
    ).values('Date').annotate(max_id=Max('id')).order_by('-Date').values_list('Date', flat=True)

    # create a dictionary to hold the marks for each date
    mark_dict = {}
    for query_date in dates:
        marks = Sec_Daily_test_mark.objects.filter(
            roll_no=roll_no,
            Date=query_date
        ).values('subject', 'mark')
        total_marks = marks.aggregate(Sum('mark'))['mark__sum']
        mark_dict[query_date] = {'marks': marks, 'total_marks': total_marks}
    context = {'roll_no': roll_no, 'mark_dict': mark_dict}
    return render(request, 'parent/mark_list.html', context)


def parentview_attendees_by_roolno(request, roll_no, class_id):
    attendees = Attendees.objects.filter(roll_no=roll_no, class_id=class_id).order_by('-Date')

    attendees_list = []
    for attendee in attendees:
        attendee_dict = {
            'Date': attendee.Date,
            'subject_states': attendee.subject_states
        }
        attendees_list.append(attendee_dict)

    context = { 
        'roll_no': roll_no,
        'class_id':class_id,
        'attendees':attendees,
        'attendeesj': json.dumps(attendees_list, cls=CustomJSONEncoder),
    }
    return render(request, 'parent/view_attendeesbyroolno.html',context)


def parent_home(request):
    if request.method == 'POST':
        role_no = request.POST.get("role_no")
        print(role_no)
        try:
            stu_id = Student.objects.get(role_no=role_no).user.id
            return redirect('parent_class_list',roll_no=role_no)
            # return render(request,'parent/parent_home.html',{'role_no':role_no,'std':obj})
        except:
            return render(request,'msg/std_doesn_exist.html')
    return render(request,'pre_home/parentsession.html')



def pview_attendees_by_roolno_graph(request, roll_no, class_id):
    attendees = Attendees.objects.filter(roll_no=roll_no,class_id=class_id).order_by('-Date')

    attendees_list = []
    for attendee in attendees:
        attendee_dict = {
            'Date': attendee.Date,
            'subject_states': attendee.subject_states
        }
        attendees_list.append(attendee_dict)

    context = {
        'roll_no': roll_no,
        'attendees':attendees,
        'attendeesj': json.dumps(attendees_list, cls=CustomJSONEncoder),
    }
    return render(request, 'parent/graph_attendees.html', context)

def pview_attendees_by_roolno_percentage(request, roll_no,class_id):
    attendees = Attendees.objects.filter(roll_no=roll_no,class_id=class_id).order_by('-Date')

    attendees_list = []
    for attendee in attendees:
        attendee_dict = {
            'Date': attendee.Date,
            'subject_states': attendee.subject_states
        }
        attendees_list.append(attendee_dict)

    context = {
        'roll_no': roll_no,
        'attendees':attendees,
        'attendeesj': json.dumps(attendees_list, cls=CustomJSONEncoder),
    }
    return render(request, 'parent/percentage_attendees.html', context)
