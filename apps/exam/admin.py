import nested_admin

from django import forms
from django.contrib import admin
from django.db import models

from .forms import AudioFormBase, ExamAdminForm, QuestionChoiceForm

# Register your models here.
from .models import Exam, Question, QuestionChoice, Score


class QuestionChoiceInline(nested_admin.NestedTabularInline):
    model = QuestionChoice
    formfield_overrides = {
        models.TextField: {"widget": forms.Textarea(attrs={"rows": 2})},
    }
    extra = 1
    form = QuestionChoiceForm
    sortable_field_name = ""


class QuestionForm(AudioFormBase):
    class Meta:
        model = Question
        exclude = ()


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    formfield_overrides = {
        models.TextField: {"widget": forms.Textarea(attrs={"rows": 3})},
    }
    extra = 1
    form = QuestionForm
    sortable_field_name = ""
    inlines = [QuestionChoiceInline]


@admin.register(Exam)
class ExamAdmin(nested_admin.NestedModelAdmin):
    form = ExamAdminForm
    list_display = (
        "title",
        "question_count",
        "exam_duration",
        "student_class",
        "created_by",
        "created_on",
        "status",
    )
    list_filter = ("student_class",)
    inlines = [QuestionInline]

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = (
        "exam",
        "candidate",
        "score",
        "has_completed",
        "start_time",
        "end_time",
    )
    list_filter = ("exam__student_class",)
    readonly_fields = ["exam", "candidate", "has_completed", "start_time", "end_time"]
