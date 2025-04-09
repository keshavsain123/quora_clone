from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Question(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class Answer(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name="liked_answers", blank=True)

    def __str__(self):
        return f"Answer to {self.question.title}"
