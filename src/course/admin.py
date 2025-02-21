from django.contrib import admin

from . models import Category, Course, CourseDocument, CourseVideo, CourseQuiz, QuizQuestion, QuizAnswer

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(CourseDocument)
admin.site.register(CourseVideo)
admin.site.register(CourseQuiz)
admin.site.register(QuizQuestion)
admin.site.register(QuizAnswer)