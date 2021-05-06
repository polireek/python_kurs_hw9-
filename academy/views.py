from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import request, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.response import Response

from LMS.settings import STUDENTS_PER_PAGE, TEACHERS_PER_PAGE, GROUPS_PER_PAGE
from .models import Group, Lecturer, Student
from .forms import AddStudentForm, AddLecturerForm, AddGroupForm, ContactForm
from .serializers import StudentSerializer, LecturerSerializer, GroupSerializer
from .tasks import send_email
from exchanger.models import ExchangeRate
from django.contrib.admin.views.decorators import staff_member_required



def index(request):
    exchange_rates = ExchangeRate.objects.all()
    context = {
        k: v for ex_rate in exchange_rates
        for k, v in ex_rate.to_dict().items()
    }
    return render(request, 'index.html', context)


def get_students(request):
    students = Student.objects.all().order_by('first_name')
    paginator = Paginator(students, STUDENTS_PER_PAGE)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)
    context = {'students': students}
    context['page'] = page
    return render(request, 'students/get_students.html',
                  context)


def get_lecturers(request):
    lecturers = Lecturer.objects.all().order_by('first_name')
    paginator = Paginator(lecturers, TEACHERS_PER_PAGE)
    page = request.GET.get('page')
    try:
        lecturers = paginator.page(page)
    except PageNotAnInteger:
        lecturers = paginator.page(1)
    except EmptyPage:
        lecturers = paginator.page(paginator.num_pages)
    context = {'lecturers': lecturers}
    context['page'] = page
    return render(request, 'lecturers/get_lecturers.html',
                  context)


def get_groups(request):
    groups = Group.objects.all().order_by('course')
    paginator = Paginator(groups, GROUPS_PER_PAGE)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)
    context = {'groups': groups}
    context['page'] = page

    return render(request, 'groups/get_groups.html',
                      context)


class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    template_name = 'form.html'
    fields = ['first_name', 'last_name', 'email', 'avatar']


class TeacherCreateView(LoginRequiredMixin, CreateView):
    model = Lecturer
    template_name = 'form.html'
    fields = ['first_name', 'last_name', 'email', 'avatar']



@staff_member_required
def add_group(request):
    form = AddGroupForm()
    if request.method == 'POST':
        comment_form = AddLecturerForm(data=request.POST)
        if comment_form.is_valid():
            new_teacher = comment_form.save(commit=False)
            new_teacher.save()

    return render(request, 'lecturers/add_lecture.html', {'form': form})


class TeacherEditView(LoginRequiredMixin, UpdateView):
    model = Lecturer
    template_name = 'form.html'
    fields = ['first_name', 'last_name', 'email', 'avatar']


class TeacherDeleteView(LoginRequiredMixin, DeleteView):
    model = Lecturer
    template_name = 'form.html'
    success_url = reverse_lazy('index')


class StudentEditView(LoginRequiredMixin, UpdateView):
    model = Student
    template_name = 'form.html'
    fields = ['first_name', 'last_name', 'email', 'avatar']


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = 'form.html'
    success_url = reverse_lazy('index')


@staff_member_required
def edit_group(request, id):
    group = get_object_or_404(Group, id=id)
    if request.method == 'POST':
        form = AddGroupForm(request.POST, instance=group)
        if form.is_valid():
            group.save()
            return redirect('get_groups')

    form = AddGroupForm(instance=group)
    return render(request, 'groups/edit_group.html', {'form': form})


@staff_member_required
def delete_group(request, id):
    Group.objects.filter(id=id).delete()
    return redirect('get_groups')


def send_message_to_email(request):
    new_message = None
    sent = request.session.get('sent', False)
    if request.method == 'POST':
        data = { 'name': "IDK", 'email': "polireek@gmail.com", 'message': "Its working"}
        if sent == False:
            request.session['sent'] = True
        send_email(data)
        print(data["email"])
        message_form = ContactForm(data=request.POST)
        if message_form.is_valid():
            new_message = message_form.save(commit=False)
            new_message.save()

    context = {
        'form': ContactForm(),
        'new_message': new_message,
        'sent' : sent
    }

    return render(request, 'contact.html', context)


@api_view(['GET', 'POST'])
def students_api(request):
    if request.method == 'GET':
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        rdata = request.data
        data = {
            'first_name': rdata.get('first_name'),
            'last_name': rdata.get('last_name'),
            'email': rdata.get('email'),
        }
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
def student_api(request):
    try:
        student = Student.objects.get(pk=id)
    except Student.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    if request.method == 'DELETE':
        student.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        first_name = request.data.get('first_name')
        if first_name:
            student.first_name = first_name
        last_name = request.data.get('last_name')
        if last_name:
            student.last_name = last_name
        email = request.data.get('email')
        if email:
            student.email = email
        student.save()
        return Response(status=HTTP_200_OK)


@api_view(['GET', 'POST'])
def lecturers_api(request):
    if request.method == 'GET':
        lecturer = Lecturer.objects.all()
        serializer = LecturerSerializer(lecturer, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        rdata = request.data
        data = {
            'first_name': rdata.get('first_name'),
            'last_name': rdata.get('last_name'),
            'email': rdata.get('email'),
        }
        serializer = LecturerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def lecturer_api(request, id):
    try:
        lecturer = Lecturer.objects.get(pk=id)
    except Lecturer.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = StudentSerializer(lecturer)
        return Response(serializer.data)

    if request.method == 'DELETE':
        lecturer.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        first_name = request.data.get('first_name')
        if first_name:
            lecturer.first_name = first_name
        last_name = request.data.get('last_name')
        if last_name:
            lecturer.last_name = last_name
        email = request.data.get('email')
        if email:
            lecturer.email = email
        lecturer.save()
        return Response(status=HTTP_200_OK)


@api_view(['GET', 'POST'])
def groups_api(request):
    if request.method == 'GET':
        group = Group.objects.all()
        serializer = GroupSerializer(group, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        rdata = request.data
        data = {
            'course': rdata.get('course'),
            'students': rdata.get('students'),
            'teacher': rdata.get('teacher'),
        }
        serializer = GroupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def group_api(request, id):
    try:
        group = Group.objects.get(id=id)
    except Group.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    if request.method == 'DELETE':
        group.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        course = request.data.get('course')
        if course:
            group.course = course
        teacher = request.data.get('teacher')
        if teacher:
            group.teacher = Lecturer.objects.get(pk=teacher)
        students = request.data.get('students')
        if students:
            group.students.set(students)
        group.save()
        return Response(status=HTTP_200_OK)