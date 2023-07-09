from django import template
import json
from dateutil.relativedelta import relativedelta
from datetime import datetime

register = template.Library()

@register.filter
def get_person_percentage(person_percentages, user_name):
    for person in person_percentages:
        if person['user_name'] == user_name:
            return person['percentage']
    return 0

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 0)

@register.filter
def tojson(value):
    return json.dumps(value)


@register.filter
def last_attendance_month(attendees):
    current_month = datetime.now().month
    last_attendance_month = None
    
    for attendee in attendees:
        attendance_month = attendee.Date.month
        if attendance_month == current_month:
            break
        last_attendance_month = attendance_month
    
    return last_attendance_month

@register.filter
def get_next_attendee(attendees, current_attendee):
    attendees_list = list(attendees)
    
    try:
        index = attendees_list.index(current_attendee)
        if index < len(attendees_list) - 1:
            return attendees_list[index + 1]
    except ValueError:
        pass
    
    return None