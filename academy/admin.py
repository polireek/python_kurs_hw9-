import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Group, Lecturer, Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email")
    actions = ['export']

    def export(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="student.csv"'
        writer = csv.writer(response)
        header = ['First Name', 'Last Name', 'Email']
        writer.writerow(header)
        for student in queryset:
            row = [student.first_name, student.last_name, student.email]
            writer.writerow(row)
        return response

    export.short_description = 'Export Students'


@admin.register(Lecturer)
class LectureAdmin(admin.ModelAdmin):
    actions = ['export']

    def export(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="lecture.csv"'
        writer = csv.writer(response)
        header = ['First Name', 'Last Name', 'Email']
        writer.writerow(header)
        for lecture in queryset:
            row = [lecture.first_name, lecture.last_name, lecture.email]
            writer.writerow(row)
        return response

    export.short_description = 'Export Lectures'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    actions = ['export']

    def export(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Groups.csv"'
        writer = csv.writer(response)
        header = ['Name', 'Lecture Name', 'Students']
        writer.writerow(header)
        for group in queryset:
            lecture_name = f'{group.teacher.first_name} {group.teacher.last_name}'
            row = [group.course, lecture_name, group.students.count()]
            writer.writerow(row)
        return response

    export.short_description = 'Export Group'
