from django.core.exceptions import ValidationError
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Project Imports
from src.base.models import AbstractInfoModel
from src.course.models import Course
from src.user.models import User


class Student(AbstractInfoModel):
    """Represents a Student model linked with the User model"""

    user = models.OneToOneField(
        User, on_delete=models.PROTECT, related_name="student_info"
    )

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")

    def __str__(self) -> str:
        """String representation of the student."""
        return self.user.email

    def send_creation_email(self):
        """Send an email to the student with their login credentials."""
        password = self.user.password  
        subject = "Your Student Account"
        message = (
            f"Hello, {self.user.first_name}!\n\n"
            f"Your account has been created. You can now log in with your email address and the following password:\n\n"
            f"Password: {password}\n\n"
            f"Please change your password after logging in for security reasons."
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[self.user.email],
        )

    def save(self, *args, **kwargs):
        is_new = self.pk is None  
        super().save(*args, **kwargs) 
        if is_new:
            self.send_creation_email()  
    
    def __str__(self) -> str:
        return self.user.email


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
        verbose_name = _("Student Enrollment")
        verbose_name_plural = _("Student Enrollments")
        unique_together = ("student", "course") 
        indexes = [models.Index(fields=["course", "student"])]

    def save(self, *args, **kwargs):
        """Ensure a student can only enroll in published courses."""
        if not self.course.is_published:
            raise ValidationError(_("Cannot enroll in an unpublished course."))
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.student.user.first_name} enrolled in {self.course.title}"
