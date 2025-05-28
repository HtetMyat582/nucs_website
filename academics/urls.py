from django.urls import path
from . import views

urlpatterns = [
    path('enroll/<int:program_id>/', views.enroll, name='enroll'),
    path('programs/', views.program_list, name='program_list'),
    path('programs/<int:pk>/', views.program_detail, name='program_detail'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
    path('faculty/', views.faculty_list, name='faculty_list'),
    path('faculty/<int:pk>/', views.faculty_detail, name='faculty_detail'),
]