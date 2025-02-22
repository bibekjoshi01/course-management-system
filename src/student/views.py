# Django Imports
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils import timezone

from src.course.models import Course

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
        user = User.objects.create_student(
            first_name=first_name,
            last_name=last_name,
            username=email,
            email=email,
            password=password,
        )

        # Create Student entry
        Student.objects.create(user=user)
        return super().form_valid(form)
    
    def test_func(self):
        """Ensure the user is an admin."""
        return self.request.user.is_staff


class StudentEnrollmentListView(ListView):
    """View for listing all student enrollments."""

    model = StudentEnrollment
    template_name = "enrollments/view_enrollments.html"
    context_object_name = "enrollments"

    def get_queryset(self):
        return StudentEnrollment.objects.filter(is_archived=False)


class StudentEnrollmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Class-based view for enrolling a student in a course."""

    model = StudentEnrollment
    form_class = StudentEnrollmentForm
    template_name = "enrollments/add_enrollment.html"
    success_url = reverse_lazy("list_enrollments")

    def form_valid(self, form):
        form.instance.created_by = self.request.user

        # Set the enrollment date
        enrollment_date = timezone.now()
        form.instance.enrollment_date = enrollment_date

        return super().form_valid(form)

    def test_func(self):
        """Ensure the user is an admin."""
        return self.request.user.is_staff


class CourseEnrollmentListView(ListView):
    model = Course
    template_name = "enrollments/course_list.html"
    context_object_name = "courses"

    def get_queryset(self):
        return Course.objects.prefetch_related("enrollments").all()


class CourseWiseEnrollmentView(DetailView):
    model = Course
    template_name = "enrollments/course_enrollments.html"
    context_object_name = "course"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        enrollments = StudentEnrollment.objects.filter(course=self.object)
        for enrollment in enrollments:
            student = enrollment.student.user
            enrollment.student_full_name = (
                student.get_full_name() if student.first_name else student.username
            )

        context["enrollments"] = enrollments
        return context
