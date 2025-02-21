from django.shortcuts import render
from django.views import View
from src.course.models import Category, Course
from src.student.models import Student, StudentEnrollment

class DashboardView(View):
    """View to represent Dashboard of the CMS"""
    
    def get(self, request):
        context = {
            "categories_count": Category.objects.filter(is_active=True).count(),
            "courses_count": Course.objects.filter(is_active=True).count(),
            "students_count": Student.objects.filter(is_active=True).count(),
            "enrollments_count": StudentEnrollment.objects.filter(is_active=True).count(),
        }
        return render(request, "home.html", context)
