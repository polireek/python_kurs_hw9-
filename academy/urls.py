from django.urls import path

from . import views

urlpatterns = [
    path('get_students/', views.get_students),
    path('get_lecturers/', views.get_lecturers),
    path('get_groups/', views.get_groups),
    path('add_student/', views.add_student),
    path('add_teacher/', views.add_teacher),
    path('add_course/', views.add_group),
]
