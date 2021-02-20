from django.shortcuts import render
from .models import Student, Lecturer, Group
from .forms import AddStudentForm, AddLecturerForm, AddCourseForm


def get_student(request):
    student = Student.objects.all().order_by('-first_name')
    return render(request, 'students/get_student.html', {'students': student})


def get_teacher(request):
    teacher = Lecturer.objects.all().order_by('-first_name')
    return render(request, 'teachers/get_teacher.html', {'teachers': teacher})


def get_course(request):
    courses = Group.objects.all().order_by('-course')
    return render(request, 'course/get_course.html', {'courses': courses})


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


def add_course(request):
    form = AddCourseForm()
    if request.method == 'POST':
        comment_form = AddCourseForm(data=request.POST)
        if comment_form.is_valid():
            new_course = comment_form.save(commit=False)
            new_course.save()

    return render(request, 'course/add_course.html', {'form': form})



