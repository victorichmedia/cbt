from django.db import models
from django.urls import reverse
from django.contrib import admin

from apps.core.models import StudentClass, User


class Exam(models.Model):
    STATUS_OPEN = 1
    STATUS_CLOSED = 2
    STATUS_CHOICES = [(STATUS_OPEN, "Open"), (STATUS_CLOSED, "Closed")]

    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    student_class = models.ForeignKey(
        StudentClass, on_delete=models.SET_NULL, null=True
    )
    duration = models.PositiveIntegerField(default=60)
    is_published = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS_CHOICES, default=STATUS_OPEN)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    @admin.display(description='Questions')
    def question_count(self):
        return self.question_set.all().count()

    def get_absolute_url(self):
        return reverse("exam-detail", kwargs={"pk": self.pk})


class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    body = models.TextField()
    audio = models.FileField(upload_to="cbt/questions/audio/", null=True, blank=True)
    image = models.ImageField(upload_to="cbt/questions/images/", null=True, blank=True)

    def __str__(self):
        return self.body[:20]


class QuestionChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    audio = models.FileField(upload_to="cbt/choices/audio/", null=True, blank=True)
    image = models.ImageField(upload_to="cbt/choices/images/", null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.body[:20]


class Score(models.Model):
    exam = models.ForeignKey(Exam, null=True, on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    has_completed = models.BooleanField(default=False)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.candidate}'s result for {self.exam}"


class UserChoice(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(QuestionChoice, on_delete=models.CASCADE, null=True)
