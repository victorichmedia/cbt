from django import forms

from .models import Exam, QuestionChoice


class AudioFormBase(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["audio"].widget.attrs.update({"capture": "", "accept": "audio/*"})


class QuestionChoiceForm(AudioFormBase):
    class Meta:
        model = QuestionChoice
        exclude = ()


class ExamAdminForm(forms.ModelForm):
    class Meta:
        model = Exam
        exclude = ("created_by",)
