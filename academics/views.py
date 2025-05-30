from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Enrollment, Course, Program, Faculty, Student
from portal.models import Event
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST
from .forms import CourseForm
from portal.forms import EventForm

@login_required
def enroll(request, program_id=None, course_id=None):
    user = request.user
    try:
        student = user.student
    except Student.DoesNotExist:
        messages.error(request, "Only students can enroll in courses.")
        return redirect('home')

    selected_program = None
    selected_course = None

    if program_id:
        selected_program = get_object_or_404(Program, pk=program_id)
    if course_id:
        selected_course = get_object_or_404(Course, pk=course_id)

    if request.method == 'POST':
        if selected_program:
            already_enrolled = Enrollment.objects.filter(student=student, program=selected_program).exists()
            if already_enrolled:
                messages.error(request, f"You are already enrolled in program: {selected_program.name}")
                return redirect('programs_and_courses')
            enrollment = Enrollment.objects.create(student=student, program=selected_program)
            messages.success(request, f"Enrolled in program: {selected_program.name}")
            return redirect('enroll_success', enrollment_id=enrollment.id)
        elif selected_course:
            already_enrolled = Enrollment.objects.filter(student=student, course=selected_course).exists()
            if already_enrolled:
                messages.error(request, f"You are already enrolled in course: {selected_course.course_name}")
                return redirect('programs_and_courses')
            enrollment = Enrollment.objects.create(student=student, course=selected_course)
            messages.success(request, f"Enrolled in course: {selected_course.course_name}")
            return redirect('enroll_success', enrollment_id=enrollment.id)
        else:
            messages.error(request, "No program or course selected for enrollment.")
            return redirect('programs_and_courses')

    return render(request, 'academics/enroll.html', {
        'selected_program': selected_program,
        'selected_course': selected_course,
    })

def programs_and_courses(request):
    programs = Program.objects.filter(is_active=True)
    courses = Course.objects.all()
    return render(request, 'academics/programs_and_courses.html', {
        'programs': programs,
        'courses': courses,
    })

def program_list(request):
    programs = Program.objects.filter(is_active=True)
    return render(request, 'academics/program_list.html', {'programs': programs})

def program_detail(request, pk):
    program = get_object_or_404(Program, pk=pk)
    return render(request, 'academics/program_detail.html', {'program': program})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'academics/course_list.html', {'courses': courses})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'academics/course_detail.html', {'course': course})

def faculty_list(request):
    faculty = Faculty.objects.all()
    return render(request, 'academics/faculty_list.html', {'faculty': faculty})

def faculty_detail(request, pk):
    faculty_member = get_object_or_404(Faculty, pk=pk)
    return render(request, 'academics/faculty_detail.html', {'faculty_member': faculty_member})

def enroll_success(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, pk=enrollment_id)
    return render(request, 'academics/enroll_success.html', {'enrollment': enrollment})

@login_required
def student_portal(request):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        messages.error(request, "Only students can access the student portal.")
        return redirect('home')

    enrollments = Enrollment.objects.filter(student=student, status='Accepted')
    programs = [enrollment.program for enrollment in enrollments if enrollment.program]
    courses = [enrollment.course for enrollment in enrollments if enrollment.course]
    events =  Event.objects.all().order_by('-date')
    context = {
        'programs': programs,
        'courses': courses,
        'student_id': request.user.username,
        'events' : events,
    }
    return render(request, 'academics/student_portal.html', context)

@login_required
def faculty_portal(request):
    try:
        faculty = request.user.faculty
    except Faculty.DoesNotExist:
        messages.error(request, "Only faculty members can access the faculty portal.")
        return redirect('home')

    courses = Course.objects.filter(faculty=faculty)
    course_students = {
        course: Enrollment.objects.filter(course=course, status='Accepted').select_related('student__user')
        for course in courses
    }
    total_students = sum(enrollments.count() for enrollments in course_students.values())
    events = Event.objects.all().order_by('-date')

    # Add forms for modals
    from .forms import CourseForm, ProgramForm
    from portal.forms import EventForm

    course_form = CourseForm()
    program_form = ProgramForm()
    event_form = EventForm()

    # For edit modals, attach a form to each object
    for course in courses:
        course.edit_form = CourseForm(instance=course)
    for event in events:
        event.edit_form = EventForm(instance=event)

    context = {
        'faculty': faculty,
        'courses': courses,
        'course_students': course_students,
        'events': events,
        'total_students': total_students,
        'course_form': course_form,
        'program_form': program_form,
        'event_form': event_form,
    }
    return render(request, 'academics/faculty_portal.html', context)


def is_faculty(user):
    return hasattr(user, 'faculty')

@login_required
@user_passes_test(is_faculty)
def faculty_add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.faculty = request.user.faculty
            course.save()
            messages.success(request, "Course created successfully.")
            return redirect('faculty_portal')
    else:
        form = CourseForm()
    return render(request, 'academics/faculty_portal.html', {'form': form})

@login_required
@user_passes_test(is_faculty)
def faculty_edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk, faculty=request.user.faculty)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully.")
            return redirect('faculty_portal')
    else:
        form = CourseForm(instance=course)
    return render(request, 'academics/faculty_portal.html', {'form': form})

@login_required
@user_passes_test(is_faculty)
@require_POST
def faculty_delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk, faculty=request.user.faculty)
    course.delete()
    messages.success(request, "Course deleted successfully.")
    return redirect('faculty_portal')

@login_required
@user_passes_test(is_faculty)
def faculty_add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Event created successfully.")
            return redirect('faculty_portal')
    else:
        form = EventForm()
    return render(request, 'academics/faculty_portal.html', {'form': form})

@login_required
@user_passes_test(is_faculty)
def faculty_edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully.")
            return redirect('faculty_portal')
    else:
        form = EventForm(instance=event)
    return render(request, 'academics/faculty_portal.html', {'form': form})

@login_required
@user_passes_test(is_faculty)
@require_POST
def faculty_delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    messages.success(request, "Event deleted successfully.")
    return redirect('faculty_portal')