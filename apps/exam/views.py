from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView

from apps.exam.models import Exam


class ExamDetailView(LoginRequiredMixin, DetailView):
    model = Exam
    template_name = "exam/exam_detail.html"
