from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Faculty', 'Faculty'),
        ('SysAdmin', 'SysAdmin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Student')
    country = CountryField(blank_label='(select country)', null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enrollment_number = models.CharField(max_length=20, null=True, blank=True)
    program = models.CharField(max_length=100, null=True, blank=True)
    year_of_study = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, null=True, blank=True)
    designation = models.CharField(max_length=100, null=True, blank=True)
    contact_info = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_or_update_student(sender, instance, created, **kwargs):
    if instance.role == 'Student':
        Student.objects.get_or_create(user=instance)
    else:
        # delete Student record if role is changed away from Student
        Student.objects.filter(user=instance).delete()

@receiver(post_save, sender=User)
def create_or_update_faculty(sender, instance, created, **kwargs):
    if instance.role == 'Faculty':
        Faculty.objects.get_or_create(user=instance)
    else:
        # delete Faculty record if role is changed away from Faculty
        Faculty.objects.filter(user=instance).delete()