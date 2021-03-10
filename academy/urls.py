from django.urls import path

from . import views

urlpatterns = [
    path('get_students/', views.get_students, name='get_students'),
    path('get_lecturers/', views.get_lecturers, name='get_lecturers'),
    path('get_groups/', views.get_groups, name='get_groups'),
    path('add_student/', views.add_student, name='add_student'),
    path('add_teacher/', views.add_teacher, name='add_teacher'),
    path('add_course/', views.add_group, name='add_course'),
    path('', views.index, name='index'),
    path('get_student/<int:id>/edit/', views.edit_student, name='edit_student'),
    path('get_student/<int:id>/delete/', views.delete_student, name='delete_student'),
    path('get_lecturer/<int:id>/edit/', views.edit_lecturer, name='edit_lecturer'),
    path('get_lecturer/<int:id>/delete/', views.delete_lecturer, name='delete_lecturer'),
    path('get_group/<int:id>/edit/', views.edit_group, name='edit_group'),
    path('get_group/<int:id>/delete/', views.delete_group, name='delete_group')
]
