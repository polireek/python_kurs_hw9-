from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=35)

    def __str__(self):
        return self.first_name+" "+self.last_name


class Lecturer(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=35)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Group(models.Model):
    course = models.CharField(max_length=20)
    students = models.ManyToManyField(Student)
    teacher = models.ForeignKey(Lecturer, on_delete=models.CASCADE)

    def __str__(self):
        return self.course
