from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField

class User(AbstractUser):
    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Faculty', 'Faculty'),
        ('SysAdmin', 'SysAdmin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Student')
    country = CountryField(blank_label='(select country)', null=True, blank=True)
    city = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment_number = models.CharField(max_length=20)
    program = models.CharField(max_length=100)
    year_of_study = models.IntegerField()

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    contact_info = models.TextField()
    