from django.urls import path

from .views import (
    StudentListView,
    StudentCreateView,
    StudentEnrollmentCreateView,
    StudentEnrollmentListView,
)
from .views import CourseEnrollmentListView, CourseWiseEnrollmentView

urlpatterns = [
    path("students/", StudentListView.as_view(), name="list_students"),
    path("add-student/", StudentCreateView.as_view(), name="add_student"),
    path("enrollments/", StudentEnrollmentListView.as_view(), name="list_enrollments"),
    path(
        "add-enrollment/", StudentEnrollmentCreateView.as_view(), name="add_enrollment"
    ),
    path("course-enrollments/", CourseEnrollmentListView.as_view(), name="course_enrollments"),
    path(
        "enrollments/<int:pk>/",
        CourseWiseEnrollmentView.as_view(),
        name="course_enrollment_detail",
    ),
]
