from src.base.constants import BaseEnum

from django.utils.translation import gettext_lazy as _


class Genders(BaseEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"
    RATHER_NOT_TO_SAY = "RATHER_NOT_TO_SAY"