from django.urls import path
from django.views.decorators.cache import cache_page

from . import views
from .views import TeacherCreateView, StudentCreateView, TeacherEditView, StudentEditView, StudentDeleteView, \
    TeacherDeleteView

urlpatterns = [
    path('get_students/', views.get_students, name='get_students'),
    path('get_lecturers/', views.get_lecturers, name='get_lecturers'),
    path('get_groups/', views.get_groups, name='get_groups'),
    path('add_student/', StudentCreateView.as_view(), name='add_student'),
    path('add_teacher/', TeacherCreateView.as_view(), name='add_teacher'),
    path('add_course/', views.add_group, name='add_course'),
    path('', views.index, name='index'),
    path('get_student/<int:pk>/edit/', cache_page(60 * 5)(StudentEditView.as_view()), name='edit_student'),
    path('get_student/<int:pk>/delete/', StudentDeleteView.as_view(), name='delete_student'),
    path('get_lecturer/<int:pk>/edit/', cache_page(60 * 5)(TeacherEditView.as_view()), name='edit_lecturer'),
    path('get_lecturer/<int:pk>/delete/', TeacherDeleteView.as_view(), name='delete_lecturer'),
    path('get_group/<int:id>/edit/', cache_page(60 * 5)(views.edit_group), name='edit_group'),
    path('get_group/<int:id>/delete/', views.delete_group, name='delete_group'),
    path('contact_us/', views.send_message_to_email, name='contact_us'),
    path('api/v1/students/', views.students_api),
    path('api/v1/student/<int:id>/', views.student_api),
    path('api/v1/lecturers/', views.lecturers_api),
    path('api/v1/lecturer/<int:id>/', views.lecturer_api),
    path('api/v1/groups/', views.groups_api),
    path('api/v1/group/<int:id>/', views.group_api),
]
