from uuid import uuid4

# Django Imports
from django.db import models
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Project Imports
from .constants import Genders
from .validators import validate_image


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            error_message = _("The given username must be set")
            raise ValueError(error_message)

        if email:
            email = self.normalize_email(email)

        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_student(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            error_message = _("Superuser must have is_staff=True.")
            raise ValueError(error_message)
        if extra_fields.get("is_superuser") is not True:
            error_message = _("Superuser must have is_superuser=True.")
            raise ValueError(error_message)

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    """
    User Model

    This model represents a user in the system,
    extending the abstract user functionality provided by Django's
    """

    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)

    phone_no = models.CharField(_("phone number"), max_length=15, blank=True)
    photo = models.ImageField(
        _("Photo"),
        validators=[validate_image],
        blank=True,
        null=True,
        default="",
    )
    gender = models.CharField(
        _("Gender"),
        max_length=50,
        choices=Genders.choices(),
        default=Genders.RATHER_NOT_TO_SAY,
    )
    is_archived = models.BooleanField(
        _("archived"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as delected. "
            "Unselect this instead of deleting users.",
        ),
    )
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(_("date updated"), auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        ordering = ["-id"]
        verbose_name = _("user")
        verbose_name_plural = _("users")
        constraints = [
            models.UniqueConstraint(
                fields=["email"],
                condition=models.Q(is_archived=False),
                name="unique_email_active_user",
            ),
        ]

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def __str__(self) -> str:
        return str(self.email)

    def get_upload_path(self, upload_path, filename) -> str:
        return f"{upload_path}/{filename}"
