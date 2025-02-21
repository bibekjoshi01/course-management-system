# Generated by Django 5.1.6 on 2025-02-21 13:49

import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import src.user.constants
import src.user.models
import src.user.validators
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                (
                    "phone_no",
                    models.CharField(
                        blank=True, max_length=15, verbose_name="phone number"
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        default="",
                        null=True,
                        upload_to="",
                        validators=[src.user.validators.validate_image],
                        verbose_name="Photo",
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("MALE", "Male"),
                            ("FEMALE", "Female"),
                            ("OTHER", "Other"),
                            ("RATHER_NOT_TO_SAY", "Rather Not To Say"),
                        ],
                        default=src.user.constants.Genders["RATHER_NOT_TO_SAY"],
                        max_length=20,
                        verbose_name="Gender",
                    ),
                ),
                (
                    "is_archived",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether this user should be treated as delected. Unselect this instead of deleting users.",
                        verbose_name="archived",
                    ),
                ),
                ("is_email_verified", models.BooleanField(default=False)),
                ("is_phone_verified", models.BooleanField(default=False)),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="date updated"),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "ordering": ["-id"],
                "constraints": [
                    models.UniqueConstraint(
                        condition=models.Q(("is_archived", False)),
                        fields=("email",),
                        name="unique_email_active_user",
                    )
                ],
            },
            managers=[
                ("objects", src.user.models.UserManager()),
            ],
        ),
    ]
