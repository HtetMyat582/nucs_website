from django.contrib import admin
from .models import Program, Course, Enrollment

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'degree_type', 'duration_years', 'is_active', 'created_at')
    search_fields = ('name', 'degree_type')
    list_filter = ('degree_type', 'is_active')
    ordering = ('-created_at',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'credits', 'faculty', 'program')
    search_fields = ('course_code', 'course_name', 'faculty')
    list_filter = ('faculty', 'program')
    ordering = ('course_code',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'program', 'course', 'enrollment_date')
    search_fields = ('student__username', 'program__name', 'course__course_name')
    list_filter = ('program', 'course')
    ordering = ('-enrollment_date',)