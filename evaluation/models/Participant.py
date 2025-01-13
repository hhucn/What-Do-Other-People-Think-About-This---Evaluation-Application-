from django.contrib.auth.models import AbstractUser
from django.db import models

from evaluation.models import Question


class Participant(AbstractUser):
    questions = models.ManyToManyField(Question, related_name='questions')
    gender = models.CharField(max_length=1000, default="None")
    education = models.CharField(max_length=1000, default="None")
    age = models.IntegerField(default=-1)
    last_accessed_question_id = models.BigIntegerField(default=-1)
    last_accessed_question_recommendation_method = models.CharField(max_length=1000, default="None")
