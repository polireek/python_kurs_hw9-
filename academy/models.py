import csv

from django.db import models
from django.db.models.signals import pre_save
from django.http import HttpResponse


class Student(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=35)
    avatar = models.ImageField(upload_to='covers/', default='covers/default.png')

    def __str__(self):
        return self.first_name+" "+self.last_name


class Lecturer(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=35)
    avatar = models.ImageField(upload_to='covers/', default='covers/default.png')

    def __str__(self):
        return self.first_name + " " + self.last_name


class Group(models.Model):
    course = models.CharField(max_length=20)
    students = models.ManyToManyField(Student)
    teacher = models.ForeignKey(Lecturer, on_delete=models.CASCADE)

    def __str__(self):
        return self.course


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=35)
    message = models.CharField(max_length=550)
    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,
            'message': self.message,
        }
