from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Enrollment, Course, Program, Student
from .forms import EnrollmentForm

@login_required
def enroll(request):
    user = request.user
    try:
        student = user.student
    except Student.DoesNotExist:
        messages.error(request, "Only students can enroll in courses.")
        return redirect('home')

    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.student = student
            enrollment.save()
            messages.success(request, "Enrollment submitted successfully!")
            return redirect('enrollments')
    else:
        form = EnrollmentForm()

    return render(request, 'academics/enroll.html', {'form': form})