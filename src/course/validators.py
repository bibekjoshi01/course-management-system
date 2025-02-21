from django.core.exceptions import ValidationError
import os


def validate_video_file(value):
    ext = os.path.splitext(value.name)[1].lower()
    if ext != '.mp4':
        raise ValidationError("Only .mp4 files are allowed.")
    if value.size > 50 * 1024 * 1024:  # 50MB
        raise ValidationError("Video file size must be less than 50MB.")


def validate_document_file(value):
    ext = os.path.splitext(value.name)[1].lower()
    if ext != '.pdf':
        raise ValidationError("Only .pdf files are allowed.")
    if value.size > 10 * 1024 * 1024:  # 10MB
        raise ValidationError("Document file size must be less than 10MB.")
