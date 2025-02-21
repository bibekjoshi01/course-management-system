from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import CreateView
from django.views.generic import ListView

from .models import Category
from .forms import CategoryForm


class AddCategoryView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories/add_category.html"
    success_url = reverse_lazy('view_categories')  # Redirect after success

    def form_valid(self, form):
        # Set the created_by field
        form.instance.created_by = self.request.user
        # Optionally, check if the user is an admin before saving
        if not self.request.user.is_staff:
            messages.error(self.request, "You do not have permission to add a category.")
            return redirect('dashboard')
        return super().form_valid(form)

    def test_func(self):
        """Ensure the user is an admin."""
        return self.request.user.is_staff



class CategoryListView(ListView):
    model = Category
    template_name = "categories/view_categories.html"
    context_object_name = 'categories'  
    paginate_by = 10  
