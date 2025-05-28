from django.urls import path
from . import views

urlpatterns = [
    path('enroll/program/<int:program_id>/', views.enroll, name='enroll_program'),
    path('enroll/course/<int:course_id>/', views.enroll, name='enroll_course'),
    path('enroll/success/<int:enrollment_id>/', views.enroll_success, name='enroll_success'),
    path('programs_and_courses/', views.programs_and_courses, name='programs_and_courses'),
    path('programs/', views.program_list, name='program_list'),
    path('programs/<int:pk>/', views.program_detail, name='program_detail'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('faculty/', views.faculty_list, name='faculty_list'),
    path('faculty/<int:pk>/', views.faculty_detail, name='faculty_detail'),
]