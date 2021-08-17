from django.urls import path

from .views import ExamDetailView, TakeExamView, ExamCompleteView

app_label = "exam"

urlpatterns = [
    path("exam/<int:pk>/detail/", ExamDetailView.as_view(), name="detail"),
    path("exam/<int:pk>/take/", TakeExamView.as_view(), name="take"),
    path("exam/<int:pk>/complete/", ExamCompleteView.as_view(), name="complete"),
]
