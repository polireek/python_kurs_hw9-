from django.test import TestCase
from django.urls import reverse
import pytest
from academy.models import Student, Lecturer, Group


class StudentViewTest(TestCase):

    NUMBER_STUDENTS = 10

    @classmethod
    def setUpTestData(cls):
        cls.firs_name = 'Ivan'
        cls.last_name = 'Ivanov'
        cls.email = "ivan_ivanov@iv.an"
        for i in range(cls.NUMBER_STUDENTS):
            Student.objects.create(
                first_name=cls.firs_name,
                last_name=cls.last_name,
                email=cls.email
            )

    def test_view_students_url(self):
        resp = self.client.get('/get_students/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('get_students'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'students/get_students.html')

    def test_view_students_url_by_name(self):
        resp = self.client.get(reverse('get_students'))
        self.assertEqual(resp.status_code, 200)


@pytest.mark.django_db
def test_student_creation():
    Student.objects.create(
        first_name='John',
        last_name='Doe',
        email='john.doe@gmail.com'
    )
    assert Student.objects.count() == 1


@pytest.mark.django_db
def test_view_students_url(client):
    resp = client.get('/get_students/')
    assert resp.status_code == 200


@pytest.mark.django_db
def test_view_students_url_by_name(client):
    resp = client.get(reverse('get_students'))
    assert resp.status_code == 200


@pytest.mark.django_db
def test_correct_context_for_students_view(client):
    Student.objects.create(
        first_name='John',
        last_name='Doe',
        email='john.doe@gmail.com'
    )
    resp = client.get(reverse('get_students'))
    assert resp.status_code == 200
    assert len(resp.context['students']) == 1


@pytest.mark.django_db
def test_unauthorized_create_student(client):
    response = client.get(reverse('add_student'))
    assert response.status_code == 302
    assert '/admin/login/' in response.url


class LecturerViewTest(TestCase):

    NUMBER_LECTURER = 10

    @classmethod
    def setUpTestData(cls):
        cls.firs_name = 'Ivan'
        cls.last_name = 'Ivanov'
        cls.email = "ivan_ivanov@iv.an"
        for i in range(cls.NUMBER_LECTURER):
            Lecturer.objects.create(
                first_name=cls.firs_name,
                last_name=cls.last_name,
                email=cls.email
            )

    def test_view_lecturer_url(self):
        resp = self.client.get('/get_lecturers/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('get_lecturers'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'lecturers/get_lecturers.html')

    def test_view_lecturer_url_by_name(self):
        resp = self.client.get(reverse('get_lecturers'))
        self.assertEqual(resp.status_code, 200)


@pytest.mark.django_db
def test_lecturer_creation():
    Lecturer.objects.create(
        first_name='John',
        last_name='Doe',
        email='john.doe@gmail.com'
    )
    assert Lecturer.objects.count() == 1


@pytest.mark.django_db
def test_view_lecturer_url(client):
    resp = client.get('/get_lecturers/')
    assert resp.status_code == 200


@pytest.mark.django_db
def test_view_lecturer_url_by_name(client):
    resp = client.get(reverse('get_lecturers'))
    assert resp.status_code == 200


@pytest.mark.django_db
def test_correct_context_for_lecturer_view(client):
    Lecturer.objects.create(
        first_name='John',
        last_name='Doe',
        email='john.doe@gmail.com'
    )
    resp = client.get(reverse('get_lecturers'))
    assert resp.status_code == 200
    assert len(resp.context['lecturers']) == 1


@pytest.mark.django_db
def test_unauthorized_create_lecturer(client):
    response = client.get(reverse('add_teacher'))
    assert response.status_code == 302
    assert '/admin/login/' in response.url


class GroupViewTest(TestCase):

    NUMBER_GROUP = 10

    @classmethod
    def setUpTestData(cls):
        cls.course = "course"
        cls.first_name = "Ivan"
        cls.last_name = "Ivanov"
        cls.email = 'ivan@ivan.ov'
        cls.teacher = Lecturer.objects.create(
            first_name=cls.first_name,
            last_name=cls.last_name,
            email=cls.email,
        )
        cls.students = Student.objects.create(
            first_name=cls.first_name,
            last_name=cls.last_name,
            email=cls.email
        )
        for i in range(cls.NUMBER_GROUP):
            group = Group.objects.create(course=cls.course, teacher=cls.teacher)
            group.students.add(cls.students)

    def test_view_lecturer_url(self):
        resp = self.client.get('/get_groups/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('get_groups'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'groups/get_groups.html')

    def test_view_lecturer_url_by_name(self):
        resp = self.client.get(reverse('get_groups'))
        self.assertEqual(resp.status_code, 200)


@pytest.mark.django_db
def test_group_creation():
    course = "course"
    first_name = "Ivan"
    last_name = "Ivanov"
    email = 'ivan@ivan.ov'
    teacher = Lecturer.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
    )
    students = Student.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email
    )
    group = Group.objects.create(course=course, teacher=teacher)
    group.students.add(students)
    assert Group.objects.count() == 1


@pytest.mark.django_db
def test_view_group_url(client):
    resp = client.get('/get_lecturers/')
    assert resp.status_code == 200


@pytest.mark.django_db
def test_view_group_url_by_name(client):
    resp = client.get(reverse('get_lecturers'))
    assert resp.status_code == 200


@pytest.mark.django_db
def test_correct_context_for_group_view(client):
    course = "course"
    first_name = "Ivan"
    last_name = "Ivanov"
    email = 'ivan@ivan.ov'
    teacher = Lecturer.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
    )
    students = Student.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email
    )
    group = Group.objects.create(course=course, teacher=teacher)
    group.students.add(students)
    resp = client.get(reverse('get_groups'))
    assert resp.status_code == 200
    assert len(resp.context['groups']) == 1


@pytest.mark.django_db
def test_unauthorized_create_group(client):
    response = client.get(reverse('add_course'))
    assert response.status_code == 302
    assert '/admin/login/' in response.url