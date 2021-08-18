from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import OuterRef, Subquery
from django.shortcuts import redirect, render
from django.views.generic import View

from apps.exam.models import Exam, Score


class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return redirect("/admin/")
        else:
            scores = Score.objects.filter(
                has_completed=True, exam=OuterRef("pk"), candidate=user
            ).values("score")
            exams = Exam.objects.filter(student_class=user.student_class).annotate(
                student_score=Subquery(scores[:1])
            )
            context = {"exams": exams}
            return render(request, "dashboard.html", context)


class LoginView(View):
    template_name = "registration/login.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.is_superuser or user.is_staff:
                        return redirect("/admin/")
                    else:
                        return redirect("dashboard")
                else:
                    messages.warning(request, "Your account is not active")
                    return redirect("login")

        messages.warning(request, "Invalid username or password")
        return redirect("login")
