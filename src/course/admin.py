from django.contrib import admin

from .models import (
    Category,
    Course,
    CourseDocument,
    CourseVideo,
    CourseQuiz,
    QuizQuestion,
    QuizAnswer,
)

admin.site.register(CourseDocument)
admin.site.register(CourseVideo)
admin.site.register(CourseQuiz)
admin.site.register(QuizQuestion)
admin.site.register(QuizAnswer)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "created_at")
