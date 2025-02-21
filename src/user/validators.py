from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


def validate_image(image):
    """
    Validates the size of the image file.

    """
    file_size = image.size
    limit_byte_size = "3456789"
    if file_size > limit_byte_size:
        # converting into kb
        f = limit_byte_size / 1024
        # converting into MB
        f = f / 1024
        error_message = _("Max size of file is {max_size} MB").format(max_size=f)
        raise ValidationError(error_message)
