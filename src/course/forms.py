from django import forms
from .models import (
    Category,
    Course,
    CourseVideo,
    CourseDocument,
    CourseQuiz,
    QuizQuestion,
    QuizAnswer,
)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "parent"]
        widgets = {
            "parent": forms.Select(attrs={"class": "form-control"}),
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter category name"}
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Category.objects.filter(name=name).exists():
            raise forms.ValidationError("This category already exists.")
        return name

    def clean(self):
        cleaned_data = super().clean()
        parent = cleaned_data.get("parent")

        # Ensure only one level of subcategories
        if parent and parent.parent:
            self.add_error(
                "parent", "A category can only have one level of subcategories."
            )

        return cleaned_data


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "description", "price", "category"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter course title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter course description",
                }
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Enter price"}
            ),
            "category": forms.Select(attrs={"class": "form-control"}),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if Course.objects.filter(title=title).exists():
            raise forms.ValidationError("This course title already exists.")
        return title


class CourseVideoForm(forms.ModelForm):
    class Meta:
        model = CourseVideo
        fields = ["title", "video_file"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter video title"}
            ),
            "video_file": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class CourseDocumentForm(forms.ModelForm):
    class Meta:
        model = CourseDocument
        fields = ["title", "document_file"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter document title"}
            ),
            "document_file": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }


class CourseQuizForm(forms.ModelForm):
    class Meta:
        model = CourseQuiz
        fields = ["title"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter quiz title"}
            )
        }


class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Enter question text"}
            )
        }


class QuizAnswerForm(forms.ModelForm):
    class Meta:
        model = QuizAnswer
        fields = ["text", "is_correct"]
        widgets = {
            "text": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter answer text"}
            ),
            "is_correct": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
