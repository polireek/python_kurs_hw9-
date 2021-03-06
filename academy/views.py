from django.shortcuts import render

from .models import Group, Lecturer, Student
from .forms import AddStudentForm, AddLecturerForm, AddGroupForm


def get_students(request):
    Students = Student.objects.all().order_by('-first_name')
    return render(request, 'students/get_students.html',
                  {'students': Students})


def get_lecturers(request):
    lecturers = Lecturer.objects.all().order_by('-first_name')
    return render(request, 'lecturers/get_lecturers.html',
                  {'lecturers': lecturers})


def get_groups(request):
    groups = Group.objects.all().order_by('-course')
    return render(request, 'groups/get_groups.html',
                  {'groups': groups})

def add_student(request):
    form = AddStudentForm()
    if request.method == 'POST':
        comment_form = AddStudentForm(data=request.POST)
        if comment_form.is_valid():
            new_student = comment_form.save(commit=False)
            new_student.save()

    return render(request, 'students/add_student.html', {'form': form})


def add_teacher(request):
    form = AddLecturerForm()
    if request.method == 'POST':
        comment_form = AddLecturerForm(data=request.POST)
        if comment_form.is_valid():
            new_teacher = comment_form.save(commit=False)
            new_teacher.save()

    return render(request, 'teachers/add_teacher.html', {'form': form})


def add_group(request):
    form = AddGroupForm()
    if request.method == 'POST':
        comment_form = AddGroupForm(data=request.POST)
        if comment_form.is_valid():
            new_course = comment_form.save(commit=False)
            new_course.save()

    return render(request, 'groups/add_group.html', {'form': form})

