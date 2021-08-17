from django.urls import path

from .views import ExamDetailView

urlpatterns = [
    path("exam-detail/<int:pk>/", ExamDetailView.as_view(), name="exam-detail"),
]
