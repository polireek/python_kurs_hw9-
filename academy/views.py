from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from .models import Group, Lecturer, Student
from .forms import AddStudentForm, AddLecturerForm, AddGroupForm, ContactForm
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
