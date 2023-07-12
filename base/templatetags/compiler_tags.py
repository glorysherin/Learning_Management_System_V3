from django import template

register = template.Library()

@register.filter
def count_lines(code):
    return len(code.split('\n'))
