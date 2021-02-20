from django.conf import settings
from django.utils.timezone import timezone
from django.db import models
from django.db.models.signals import pre_save


class Student (models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    def __str__(self):
        return str(self.first_name + " " + self.last_name + " " + self.email + " ")


class Lecturer (models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return str(self.first_name+" "+self.last_name+" "+ self.email+" ")


class Group (models.Model):
    id = models.AutoField(primary_key=True)
    course = models.CharField(max_length=100)
    students = models.ForeignKey(Student, related_name='Student', on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(Lecturer, related_name='Lecturer', on_delete=models.CASCADE, null=True)


    def __str__(self):
        return str(self.first_name)

