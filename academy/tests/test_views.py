from django.test import TestCase
from django.urls import reverse

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