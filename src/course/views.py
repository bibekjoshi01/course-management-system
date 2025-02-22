from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView

# Project Imports
from .models import Category
from .forms import CategoryForm
from .models import Course, QuizQuestion, QuizAnswer
from .forms import (
    CourseForm,
    CourseVideoForm,
    CourseDocumentForm,
    CourseQuizForm,
)


class CategoryListView(ListView):
    """View to list all categories"""

    model = Category
    template_name = "categories/view_categories.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.filter(is_archived=False)


class AddCategoryView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """View to add new category"""

    model = Category
    form_class = CategoryForm
    template_name = "categories/add_category.html"
    success_url = reverse_lazy("list_categories")  
    login_url = "/admin/login/"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """Ensure the user is an admin."""
        return self.request.user.is_staff


class AddCourseView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """View to add a new course along with related videos, documents, and quizzes."""

    model = Course
    form_class = CourseForm
    template_name = "courses/add_course.html"
    success_url = reverse_lazy("view_courses")  # Redirect after success
    login_url = "/admin/login/"

    def form_valid(self, form):
        # Set the created_by field for the course
        form.instance.created_by = self.request.user
        course = form.save()
        self._handle_related_objects(course)

        return super().form_valid(form)

    def _handle_related_objects(self, course):
        # Handle course video
        video_form = CourseVideoForm(self.request.POST, self.request.FILES)
        if video_form.is_valid():
            video_form.instance.course = course
            video_form.save()

        # Handle course document
        document_form = CourseDocumentForm(self.request.POST, self.request.FILES)
        if document_form.is_valid():
            document_form.instance.course = course
            document_form.save()

        # Handle quiz and questions
        quiz_form = CourseQuizForm(self.request.POST)
        if quiz_form.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.course = course
            quiz.save()

            questions = self.request.POST.getlist("questions")  # Get questions data
            for question_text in questions:
                quiz_question = QuizQuestion(quiz=quiz, text=question_text)
                quiz_question.save()

            answers = self.request.POST.getlist("answers")  # Get answers data
            for answer_text in answers:
                quiz_answer = QuizAnswer(quiz_question=quiz_question, text=answer_text)
                quiz_answer.save()

    def test_func(self):
        """Ensure the user is an admin."""
        return self.request.user.is_staff


class CourseListView(ListView):
    """View to list courses"""
    
    model = Course
    template_name = "courses/view_courses.html"
    context_object_name = "courses"
