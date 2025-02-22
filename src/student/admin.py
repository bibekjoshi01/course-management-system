from django.contrib import admin

from .models import Student, StudentEnrollment


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Custom admin for Student model."""
    
    list_display = (
        "user_first_name", 
        "user_last_name", 
        "user_email", 
        "is_enrolled_in_any_course"
    )

    def user_first_name(self, obj):
        return obj.user.first_name
    
    def user_last_name(self, obj):
        return obj.user.last_name
    
    def user_email(self, obj):
        return obj.user.email

    def is_enrolled_in_any_course(self, obj):
        """Return True if the student is enrolled in any course."""
        return obj.enrollments.exists()
    
    user_first_name.short_description = 'First Name'
    user_last_name.short_description = 'Last Name'
    user_email.short_description = 'Email'
    is_enrolled_in_any_course.boolean = True 
    is_enrolled_in_any_course.short_description = 'Enrolled in Any Course'


@admin.register(StudentEnrollment)
class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrollment_date")
    list_filter = ("course",)
