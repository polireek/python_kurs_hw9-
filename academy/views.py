from django.shortcuts import render
from django.http import HttpResponse
from .models import Student,Lecturer,Group

def get_students(request):
    Students = Student.objects.all().order_by('-first_name')
    return render(request, 'students/get_students.html', {'students': Students})

def get_lecturers(request):
    lecturers = Lecturer.objects.all().order_by('-first_name')
    return render(request, 'lecturers/get_lecturers.html', {'lecturers': lecturers})

def get_groups(request):
    groups = Group.objects.all().order_by('-course')
    return render(request, 'groups/get_groups.html', {'groups': groups})

