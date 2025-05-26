from django import forms
from .models import Enrollment

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['program', 'course']
        widgets = {
            'program': forms.Select(attrs={'class': 'form-input select'}),
            'course': forms.Select(attrs={'class': 'form-input select'}),
        }