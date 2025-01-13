from django.contrib import admin

from evaluation.models import Participant, Question, PointOfViewSetAnswer, CommentSelection, Comment
from evaluation.models.AnswerRepository import CommentAnswer

# Register your models here.

admin.site.register(Participant)
admin.site.register(Question)
admin.site.register(CommentSelection)
admin.site.register(Comment)
admin.site.register(PointOfViewSetAnswer)
admin.site.register(CommentAnswer)
