from django import forms

from .models import Student, Lecturer, Group


class AddStudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ('first_name',
                  'last_name',
                  "email",
                  )


class AddLecturerForm(forms.ModelForm):

    class Meta:
        model = Lecturer
        fields = ('first_name',
                  'last_name',
                  "email",
                  )


class AddGroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ('course',
                  'students',
                  "teacher",
                  )