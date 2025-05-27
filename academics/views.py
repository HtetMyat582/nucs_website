from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Enrollment, Course, Program, Student

@login_required
def enroll(request):
    user = request.user
    try:
        student = user.student
    except Student.DoesNotExist:
        messages.error(request, "Only students can enroll in courses.")
        return redirect('home')

    if request.method == 'POST':
        program_id = request.POST.get('program_id')
        course_id = request.POST.get('course_id')

        if not program_id and not course_id:
            messages.error(request, "You must select either a program or a course to enroll in.")
            return redirect('enroll')

        if program_id:
            program = Program.objects.get(pk=program_id)
            Enrollment.objects.create(student=student, program=program)
            messages.success(request, f"Enrolled in program: {program.name}")
        elif course_id:
            course = Course.objects.get(pk=course_id)
            Enrollment.objects.create(student=student, course=course)
            messages.success(request, f"Enrolled in course: {course.course_name}")

        return redirect('enrollments')

    programs = Program.objects.filter(is_active=True)
    courses = Course.objects.all()
    return render(request, 'academics/enroll.html', {
        'programs': programs,
        'courses': courses,
    })