from django.shortcuts import render, get_object_or_404, redirect

from .models import Group, Lecturer, Student
from .forms import AddStudentForm, AddLecturerForm, AddGroupForm




def index(request):
    return render(request, 'index.html')


def get_students(request):
    students = Student.objects.all().order_by('first_name')
    return render(request, 'students/get_students.html',
                  {'students': students})


def get_lecturers(request):
    lecturers = Lecturer.objects.all().order_by('first_name')
    return render(request, 'lecturers/get_lecturers.html',
                  {'lecturers': lecturers})


def get_groups(request):
    groups = Group.objects.all().order_by('course')
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

    return render(request, 'lecturers/add_lecture.html', {'form': form})


def add_group(request):
    form = AddGroupForm()
    if request.method == 'POST':
        comment_form = AddLecturerForm(data=request.POST)
        if comment_form.is_valid():
            new_teacher = comment_form.save(commit=False)
            new_teacher.save()

    return render(request, 'lecturers/add_lecture.html', {'form': form})


def edit_lecturer(request, id):
    lecturer = get_object_or_404(Lecturer, id=id)
    if request.method == 'POST':
        form = AddLecturerForm(request.POST, instance=lecturer)
        if form.is_valid():
            lecturer.save()
            return redirect('get_lecturers')

    form = AddLecturerForm(instance=lecturer)
    return render(request, 'lecturers/edit_lecture.html', {'form': form})


def delete_lecturer(request, id):
    Lecturer.objects.filter(id=id).delete()
    return redirect('get_lecturers')


def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        form = AddStudentForm(request.POST, instance=student)
        if form.is_valid():
            student.save()
            return redirect('get_students')

    form = AddStudentForm(instance=student)
    return render(request, 'students/edit_student.html', {'form': form})


def delete_student(request, id):
    Student.objects.filter(id=id).delete()
    return redirect('get_students')


def edit_group(request, id):
    group = get_object_or_404(Group, id=id)
    if request.method == 'POST':
        form = AddGroupForm(request.POST, instance=group)
        if form.is_valid():
            group.save()
            return redirect('get_groups')

    form = AddGroupForm(instance=group)
    return render(request, 'groups/edit_group.html', {'form': form})


def delete_group(request, id):
    Group.objects.filter(id=id).delete()
    return redirect('get_groups')