from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, View

from apps.exam.models import Exam


class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return redirect("/admin/")
        else:
            exams = Exam.objects.filter(student_class=user.student_class)
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
