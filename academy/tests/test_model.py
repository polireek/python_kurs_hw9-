from django.contrib.auth.models import User
from django.test import TestCase
import pytest
from django.core.exceptions import ValidationError

from academy.models import Student, Lecturer, Group


class StudentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.first_name = "Ivan"
        cls.last_name = "Ivanov"
        cls.email = "ivan_ivanov@iv.an"
        cls.user = User.objects.create_user(username="admin")

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_successful_student_create(self):
        student = Student(first_name=self.first_name, last_name=self.last_name, email=self.email)
        student.full_clean()

    def test_max_first_name_charts(self):
        student = Student(first_name="a" * 51, last_name=self.last_name, email=self.email)
        with self.assertRaises(ValidationError):
            student.full_clean()

    def test_none_last_name(self):
        student = Student(first_name=self.first_name, last_name=None, email=self.email)
        student.full_clean()




class LecturerModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.first_name = "Ivan"
        cls.last_name = "Ivanov"
        cls.email = "ivan_ivanov@iv.an"
        cls.user = User.objects.create_user(username="admin")

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_successful_teacher_create(self):
        teacher = Lecturer(first_name=self.first_name, last_name=self.last_name, email=self.email)
        teacher.full_clean()

    def test_max_first_name_charts(self):
        teacher = Lecturer(first_name="a" * 51, last_name=self.last_name, email=self.email)
        with self.assertRaises(ValidationError):
            teacher.full_clean()

    def test_none_last_name(self):
        teacher = Lecturer(first_name=self.first_name, last_name=None, email=self.email)
        teacher.full_clean()


class GroupModelTest(TestCase):

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
        cls.user = User.objects.create_user(username="admin")

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_successful_group_create(self):
        group = Group.objects.create(course=self.course, teacher=self.teacher)
        group.students.add(self.students)
        group.full_clean()

    def test_max_course_charts(self):
        group = Group.objects.create(course="a" * 51, teacher=self.teacher)
        group.students.add(self.students)
        with self.assertRaises(ValidationError):
            group.full_clean()

    def test_none_students_name(self):
        group = Group.objects.create(course=self.course, teacher=self.teacher)
        group.full_clean()