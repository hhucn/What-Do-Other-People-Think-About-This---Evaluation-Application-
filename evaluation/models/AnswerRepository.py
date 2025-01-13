from django.db import models

from evaluation.models import Question, CommentSelection, Comment
from evaluation.models.CommentRepository import CommentSelectionRepository
from evaluation.models.Participant import Participant


class AnswerRepository:
    @staticmethod
    def save_point_of_view_set_answer(participant_id, question_id, recommendation_method: str, selected_method: str):
        db_question = Question.objects.get(pk=question_id)
        db_participant = Participant.objects.get(pk=participant_id)
        PointOfViewSetAnswer.objects.create(question=db_question, participant=db_participant, recommendation_method=recommendation_method, selected_method=selected_method)
        db_participant.last_accessed_question_id = -1
        db_participant.last_accessed_question_recommendation_method = "None"
        db_participant.save()

    @staticmethod
    def save_comment_answer(participant_id, question_id, comment_id, good_recommendation):
        participant = Participant.objects.get(pk=participant_id)
        question = Question.objects.get(pk=question_id)
        comment = Comment.objects.get(pk=comment_id)
        comment_selection = comment.comment_selection
        CommentAnswer.objects.create(participant=participant, question=question, comment_selection=comment_selection, comment=comment, good_recommendation=good_recommendation)


class PointOfViewSetAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="PointOfViewAnswers")
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="PointOfViewAnswers")
    recommendation_method = models.CharField(max_length=1000)
    selected_method = models.CharField(max_length=1000)

    class Meta:
        unique_together = ('question', 'participant', 'recommendation_method', 'selected_method')


class CommentAnswer(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="CommentAnswers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="CommentAnswers")
    comment_selection = models.ForeignKey(CommentSelection, on_delete=models.CASCADE, related_name="CommentAnswers")
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="CommentAnswer")
    good_recommendation = models.BooleanField(default=False)

    class Meta:
        unique_together = ('question', 'participant', 'comment_selection', 'comment')
