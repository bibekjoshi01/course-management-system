# Django Imports
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.utils import timezone

# Project Imports
from .models import Student, StudentEnrollment
from src.user.models import User
from .forms import StudentEnrollmentForm, StudentForm
from .utils import generate_strong_password


class StudentListView(ListView):
    """View to list all students"""

    model = Student
    template_name = "students/student_list.html"
    context_object_name = "students"

    def get_queryset(self):
        return Student.objects.filter(is_archived=False)


class StudentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """View to create a new student"""

    model = Student
    form_class = StudentForm
    template_name = "students/add_student.html"
    success_url = reverse_lazy("list_students")

    def form_valid(self, form):
        """Handling student creation and email sending"""

        email = form.cleaned_data["email"]
        first_name = form.cleaned_data["first_name"].strip().title()
        last_name = form.cleaned_data["last_name"].strip().title()
        form.instance.created_by = self.request.user

        # Generate strong random password
        password = generate_strong_password()

        # Create User model entry
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=email,
            email=email,
            password=make_password(password),
        )

        # Create Student entry
        Student.objects.create(user=user)

        # Send email with login credentials
        send_mail(
            subject="Your Student Account",
            message=f"Hello, {first_name}! Your account has been created. Your password is: {password}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return super().form_valid(form)

    def test_func(self):
        """Ensure the user is an admin."""
        return self.request.user.is_staff


class StudentEnrollmentListView(ListView):
    """View for listing all student enrollments."""

    model = StudentEnrollment
    template_name = "students/enrollment_list.html"
    context_object_name = "enrollments"

    def get_queryset(self):
        return StudentEnrollment.objects.filter(is_archived=False)


class StudentEnrollmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Class-based view for enrolling a student in a course."""

    model = StudentEnrollment
    form_class = StudentEnrollmentForm
    template_name = "students/enroll_student.html"
    success_url = reverse_lazy("list_enrollments")

    def form_valid(self, form):
        """Handling student creation."""

        student = form.cleaned_data["student"]
        course = form.cleaned_data["course"]
        form.instance.created_by = self.request.user

        if StudentEnrollment.objects.filter(student=student, course=course).exists():
            form.add_error(None, "This student is already enrolled in this course.")
            return self.form_invalid(form)

        # Set the enrollment date
        enrollment_date = timezone.now()
        form.instance.enrollment_date = enrollment_date

        return super().form_valid(form)
