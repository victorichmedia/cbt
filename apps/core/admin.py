from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import StudentClass, Subject, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("fullname", "username", "student_class", "is_staff", "is_superuser")
    list_filter = ("is_staff", "is_superuser", "student_class")
    filter_horizontal = []
    search_fields = (
        "fullname",
        "username",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                )
            },
        ),
        (
            "Profile",
            {"fields": ("fullname", "email", "student_class",)},
        ),
        ("Others", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = ((None, {"fields": ("username", "password1", "password2")}),)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")


@admin.register(StudentClass)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")
