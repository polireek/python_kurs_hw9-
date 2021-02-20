from django.urls import path

from . import views

urlpatterns = [
    path('students/', views.get_student),
    path('teachers/', views.get_teacher),
    path('courses/', views.get_course),
    path('add_student/', views.add_student),
    path('add_teacher/', views.add_teacher),
    path('add_course/', views.add_course),

]
