from academics.models import Enrollment
from users.models import Student, Faculty

def has_accepted_enrollment(request):
    if request.user.is_authenticated:
        try:
            student = request.user.student
            return {
                'has_accepted_enrollment': Enrollment.objects.filter(student=student, status='Accepted').exists()
            }
        except Student.DoesNotExist:
            pass
    return {'has_accepted_enrollment': False}

def is_faculty(request):
    if request.user.is_authenticated:
        try:
            request.user.faculty
            return {'is_faculty': True}
        except Faculty.DoesNotExist:
            pass
    return {'is_faculty': False}