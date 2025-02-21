from django.urls import path
from .views import AddCategoryView, CategoryListView

urlpatterns = [
    path('add-category/', AddCategoryView.as_view(), name='add_category'),
    path('categories/', CategoryListView.as_view(), name='view_categories'),
]
