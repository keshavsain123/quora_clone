from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm, SignUpForm


def home(request):
    questions = Question.objects.all().order_by("-created_at")
    return render(request, "core/home.html", {"questions": questions})


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "core/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
    return render(request, "core/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def post_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.created_by = request.user
            question.save()
            return redirect("home")
    else:
        form = QuestionForm()
    return render(request, "core/post_question.html", {"form": form})


def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = Answer.objects.filter(question=question)
    form = AnswerForm()
    return render(
        request,
        "core/question_detail.html",
        {"question": question, "answers": answers, "form": form},
    )


@login_required
def post_answer(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.created_by = request.user
            answer.save()
    return redirect("question_detail", pk=pk)


@login_required
def like_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    answer.likes.add(request.user)
    return redirect("question_detail", pk=answer.question.pk)
