from django.urls import path
from .views import AddCategoryView, AddCourseView, CategoryListView, CourseListView

urlpatterns = [
    path("add-category/", AddCategoryView.as_view(), name="add_category"),
    path("categories/", CategoryListView.as_view(), name="view_categories"),
    path("add-course/", AddCourseView.as_view(), name="add_course"),
    path("courses/", CourseListView.as_view(), name="view_courses"),
]
