from django import forms
from .models import Question, Answer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title", "description"]


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["content"]


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
