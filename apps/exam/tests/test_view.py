from django.test import TestCase
from django.urls import reverse

from apps.core.models import StudentClass, User
from apps.exam.models import Exam


class ExamDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        student_class = StudentClass.objects.create(name="cls")
        cls.exam = Exam.objects.create(
            code="001", title="test_exam", student_class=student_class
        )
        cls.admin = User.objects.get(pk=1)
        cls.student = User.objects.create_user(
            username="student",
            password="pass",
            fullname="adrew",
        )

    def setUp(self):
        self.client.force_login(self.admin)

    def test_exam_detail(self):
        response = self.client.get(reverse("exam-detail", kwargs={"pk": self.exam.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "exam/exam_detail.html")
