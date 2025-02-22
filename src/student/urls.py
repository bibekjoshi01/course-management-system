from django.urls import path

from .views import (
    StudentListView,
    StudentCreateView,
    StudentEnrollmentCreateView,
    StudentEnrollmentListView,
)

urlpatterns = [
    path("students/", StudentListView.as_view(), name="list_students"),
    path("add-student/", StudentCreateView.as_view(), name="add_student"),
    path("enrollments/", StudentEnrollmentListView.as_view(), name="list_enrollments"),
    path(
        "add-enrollment/", StudentEnrollmentCreateView.as_view(), name="add_enrollment"
    ),
]
