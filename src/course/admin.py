from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import (
    Category,
    Course,
    CourseDocument,
    CourseVideo,
    CourseQuiz,
    QuizQuestion,
    QuizAnswer,
)


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ("name", "parent", "level", "is_leaf_node")
    search_fields = ("name",)
    list_filter = ("parent",)
    ordering = ("parent", "name")
    list_select_related = ("parent",)

    def is_leaf_node(self, obj):
        return obj.is_leaf_node()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related("subcategories")

    def save_model(self, request, obj, form, change):
        obj.clean()
        super().save_model(request, obj, form, change)

    def parent_category(self, obj):
        return obj.parent.name if obj.parent else "None"

    is_leaf_node.boolean = True
    is_leaf_node.short_description = "Is Leaf Node"
    parent_category.short_description = "Parent Category"


class CourseVideoInline(admin.TabularInline):
    model = CourseVideo
    extra = 1
    fields = ("title", "video_file", "order")
    ordering = ["order"]


class CourseDocumentInline(admin.TabularInline):
    model = CourseDocument
    extra = 1
    fields = ("title", "document_file", "order")
    ordering = ["order"]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Custom admin for Course model with its sub-modules."""

    list_display = ("title", "category", "price", "is_published", "created_at")
    list_filter = ("is_published", "category")
    search_fields = ("title",)
    ordering = ("category", "title")

    inlines = [CourseVideoInline, CourseDocumentInline]
    

class QuizAnswerInline(admin.TabularInline):
    model = QuizAnswer
    extra = 1  
    fields = ("text", "is_correct")
    
    
@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ("quiz", "text", "created_at")
    list_filter = ("quiz",)
    search_fields = ("text",)
    ordering = ("quiz", "text")

    inlines = [QuizAnswerInline]


@admin.register(CourseQuiz)
class CourseQuizAdmin(admin.ModelAdmin):
    list_display = ("course", "title", "created_at")
    list_filter = ("course",)
    search_fields = ("title",)
    ordering = ("course", "title")
    
