from django.urls import path

from .views import ExamCompleteView, ExamDetailView, TakeExamView, ScoreDetailView

app_name = "exam"

urlpatterns = [
    path("exam/<int:pk>/detail/", ExamDetailView.as_view(), name="detail"),
    path("exam/<int:pk>/take/", TakeExamView.as_view(), name="take"),
    path("exam/<int:pk>/complete/", ExamCompleteView.as_view(), name="complete"),
    path("exam/<int:pk>/complete/", ScoreDetailView.as_view(), name="score-detail"),
]
