"""
URL configuration for config project.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from .views import DashboardView


urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", TemplateView.as_view(template_name="home.html"), name="dasboard"),
    path("", DashboardView.as_view(), name="dashboard"),
    path("course/", include("src.course.urls"), name="course"),
    # Media files
    * static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
