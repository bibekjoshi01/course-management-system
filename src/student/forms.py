from django import forms
from django.core.exceptions import ValidationError

# Project Imports
from src.user.models import User
from src.course.models import Course
from .models import StudentEnrollment, Student


class StudentForm(forms.ModelForm):
    """Form to register a new student"""

    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = Student
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        """Ensure email is unique in the User model"""
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")

        return email


class StudentEnrollmentForm(forms.ModelForm):
    """Form for enrolling a student in a course."""

    class Meta:
        model = StudentEnrollment
        fields = ["student", "course"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter courses to only show published and active courses
        self.fields["course"].queryset = Course.objects.filter(
            is_published=True, is_active=True
        )
