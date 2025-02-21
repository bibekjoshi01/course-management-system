# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Project Imports
from src.base.models import AbstractInfoModel
from src.course.models import Course
from src.user.models import User


class Student(AbstractInfoModel):
    """Represents a Student model linked with User model"""

    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name="student")

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")

    def __str__(self) -> str:
        return self.user.first_name


class StudentEnrollment(AbstractInfoModel):
    """Represents an enrollment of a student in a course."""

    student = models.ForeignKey(
        Student, on_delete=models.PROTECT, related_name="enrollments"
    )
    course = models.ForeignKey(
        Course, on_delete=models.PROTECT, related_name="enrollments"
    )
    enrollment_date = models.DateTimeField(_("Enrollment Date"), auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")

    def __str__(self) -> str:
        return f"{self.student.user.first_name} enrolled in {self.course.title}"
