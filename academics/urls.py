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
    path('student/portal/', views.student_portal, name='student_portal'),
    path('faculty/portal/', views.faculty_portal, name='faculty_portal'),
    path('faculty/add_course/', views.faculty_add_course, name='faculty_add_course'),
    path('faculty/edit_course/<int:pk>/', views.faculty_edit_course, name='faculty_edit_course'),
    path('faculty/add_event/', views.faculty_add_event, name='faculty_add_event'),
    path('faculty/edit_event/<int:pk>/', views.faculty_edit_event, name='faculty_edit_event'),
    path('faculty/course/<int:pk>/delete/', views.faculty_delete_course, name='faculty_delete_course'),
    path('faculty/event/<int:pk>/delete/', views.faculty_delete_event, name='faculty_delete_event'),

]