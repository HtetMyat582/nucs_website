from django.db import models
from users.models import Student, Faculty

class Program(models.Model):
    DEGREE_CHOICES = [
        ('Bachelors', 'Bachelors'),
        ('Masters', 'Masters'),
        ('PhD', 'PhD'),
    ]
    name = models.CharField(max_length=100, unique=True)
    degree_type = models.CharField(max_length=20, choices=DEGREE_CHOICES, default='Bachelors')
    description = models.TextField(blank=True)
    duration_years = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    program = models.ForeignKey(
        Program, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses'
    )
    course_code = models.CharField(max_length=10)
    course_name = models.CharField(max_length=100)
    description = models.TextField()
    credits = models.IntegerField()
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)