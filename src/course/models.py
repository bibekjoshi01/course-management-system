# Django Imports
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

# Project Imports
from src.base.models import AbstractInfoModel
from .validators import validate_document_file, validate_video_file


class Category(AbstractInfoModel, MPTTModel):
    """Category Model with Parent-Child Relationship"""

    name = models.CharField(
        _("Name"), max_length=255, unique=True, help_text=_("Name of the category.")
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="subcategories",
        help_text=_("Parent category if this is a subcategory."),
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def clean(self):
        """Enforce only 2 levels in category hierarchy"""

        if self.parent and self.parent.parent:
            raise ValidationError(
                _("A category can only have one level of subcategories.")
            )

    def save(self, *args, **kwargs):
        # Ensure validation runs before saving
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name if not self.parent else f"{self.parent} → {self.name}"


class Course(AbstractInfoModel):
    """Represents a Course Model"""

    title = models.CharField(
        _("Title"),
        max_length=255,
        db_index=True,
        help_text=_("Title of the course."),
    )
    description = models.TextField(
        _("Description"), help_text=_("Detailed course description.")
    )
    price = models.DecimalField(
        _("Price"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text=_("Price of the course. Must be non-negative."),
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="courses",
        help_text=_("Category to which the course belongs."),
    )
    is_published = models.BooleanField(
        _("Publised"), default=True, help_text="whether the course is published or not."
    )

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
        ]
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def __str__(self) -> str:
        return self.title


class CourseVideo(AbstractInfoModel):
    """Represents a Video associated with a Course."""

    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        related_name="videos",
        help_text=_("The course to which this video belongs."),
    )
    title = models.CharField(
        _("Title"),
        max_length=255,
        db_index=True,
        help_text=_("Title of the video."),
    )
    video_file = models.FileField(
        _("Video File"),
        upload_to="course/videos/",
        validators=[validate_video_file],
        help_text=_("Upload only .mp4 files with a maximum size of 50MB."),
    )
    order = models.PositiveIntegerField(
        _("Order"),
        default=0,
        help_text=_("Defines the sequence of this content in the course."),
    )

    class Meta:
        verbose_name = _("Course Video")
        verbose_name_plural = _("Course Videos")
        ordering = ["order"]

    def __str__(self) -> str:
        return self.title


class CourseDocument(AbstractInfoModel):
    """Represents a Document related to a Course."""

    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        related_name="documents",
        help_text=_("The course to which this document belongs."),
    )
    title = models.CharField(
        _("Title"),
        max_length=255,
        db_index=True,
        help_text=_("Title of the document."),
    )
    document_file = models.FileField(
        _("Document File"),
        upload_to="course/documents/",
        validators=[validate_document_file],
        help_text=_("Upload only .pdf files with a maximum size of 10MB."),
    )
    order = models.PositiveIntegerField(
        _("Order"),
        default=0,
        help_text=_("Defines the sequence of this content in the course."),
    )
    
    class Meta:
        verbose_name = _("Course Document")
        verbose_name_plural = _("Course Documents")
        ordering = ["order"]

    def __str__(self) -> str:
        return self.title


class CourseQuiz(AbstractInfoModel):
    """Represents a Quiz related to a Course."""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="quizzes")
    title = models.CharField(
        _("Quiz Title"),
        max_length=255,
        db_index=True,
        help_text=_("Title of the quiz."),
    )

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")

    def __str__(self) -> str:
        return self.title


class QuizQuestion(AbstractInfoModel):
    """Represents a Question associated with a Quiz."""

    quiz = models.ForeignKey(
        CourseQuiz, on_delete=models.CASCADE, related_name="questions"
    )
    text = models.TextField(
        _("Question Text"),
        help_text=_("Text of the question."),
    )

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self) -> str:
        return self.text[:100]


class QuizAnswer(AbstractInfoModel):
    """Represents an Answer associated with a Question."""

    question = models.ForeignKey(
        QuizQuestion, on_delete=models.CASCADE, related_name="answers"
    )
    text = models.CharField(
        _("Answer Text"),
        max_length=255,
        help_text=_("Answer option text."),
    )
    is_correct = models.BooleanField(
        _("Is Correct?"),
        default=False,
        help_text=_("Mark if this answer is correct."),
    )

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")


    def __str__(self) -> str:
        return f"{self.text} ({'Correct' if self.is_correct else 'Wrong'})"