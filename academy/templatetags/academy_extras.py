from django import template

register = template.Library()


@register.filter()
def get_students(students):
    return students.count()
