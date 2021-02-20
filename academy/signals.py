from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Student, Lecturer, Group


@receiver(pre_save, sender=Student)
def add_suspicious_comment(sender, instance, **kwargs):
    instance.first_name = instance.first_name.capitalize()
    instance.last_name = instance.last_name.capitalize()


@receiver(pre_save, sender=Lecturer)
def add_suspicious_comment(sender, instance, **kwargs):
    instance.first_name = instance.first_name.capitalize()
    instance.last_name = instance.last_name.capitalize()


@receiver(pre_save, sender=Group)
def add_suspicious_comment(sender, instance, **kwargs):
    instance.course = instance.course.capitalize()
