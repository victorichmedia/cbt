from datetime import timedelta

from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import DetailView, View

from apps.exam.models import Exam, Question, Score, UserChoice


class ExamDetailView(LoginRequiredMixin, DetailView):
    model = Exam
    template_name = "exam/exam_detail.html"


class TakeExamView(LoginRequiredMixin, View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.exam = Exam.objects.get(pk=kwargs["pk"])
        self.questions = (
            Question.objects.filter(exam=self.exam)
            .prefetch_related("questionchoice_set")
            .order_by("?")
        )
        self.score, created = Score.objects.get_or_create(
            exam=self.exam,
            candidate=request.user,
        )

    def get(self, request, *args, **kwargs):
        exam = self.exam
        score = self.score
        alloted = timedelta(minutes=exam.duration)
        newtime = score.start_time + alloted

        context = {
            "questions": self.questions,
            "exam": exam,
            "score": score,
            "time": newtime,
        }
        return render(request, "exam/take.html", context)

    def post(self, request, *args, **kwargs):
        user_choices = []
        data = request.POST
        for question in self.questions:
            q_id = str(question.id)
            if data.getlist(q_id):
                user_choices.append(
                    UserChoice(
                        exam=self.exam,
                        question=question,
                        candidate=request.user,
                        choice_id=data[q_id],
                    )
                )
        UserChoice.objects.bulk_create(user_choices)

        number_of_correct_choices = UserChoice.objects.filter(
            exam=self.exam, candidate=request.user, choice__is_correct=True
        ).count()

        score = self.score
        score.has_completed = True
        score.score = int((number_of_correct_choices / len(self.questions)) * 100)
        score.end_time = timezone.now()
        score.save()

        return redirect("exam:complete", self.exam.id)


class ExamCompleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        exam = Exam.objects.get(id=kwargs["pk"])
        score = Score.objects.get(exam=exam, candidate=request.user)
        context = {
            "exam": exam,
            "score": score,
        }
        return render(request, "exam/complete.html", context)


class ScoreDetailView(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
        score = Score.objects.get(exam=kwargs["pk"], candidate=request.user)
        context = {
            "score": score,
        }
        return render(request, "exam/score_detail.html", context)