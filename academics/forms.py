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

    def clean(self):
        cleaned_data = super().clean()
        program = cleaned_data.get('program')
        course = cleaned_data.get('course')

        if program and course:
            raise forms.ValidationError("You can enroll in either a program or a course, not both.")
        if not program and not course:
            raise forms.ValidationError("You must select either a program or a course to enroll in.")
        return cleaned_data