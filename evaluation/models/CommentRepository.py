import random

from django.db import models

from evaluation.domain.CommentSuggestion import CommentSuggestion as DomainCommentSuggestion
from evaluation.models import Question
from evaluation.models.utils.clean_text import remove_html_tags


class CommentSelection(models.Model):
    recommendation_method = models.CharField(max_length=100, default="Suggestion")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="comment_selection")

    def __str__(self):
        return self.recommendation_method


class Comment(models.Model):
    text = models.CharField(max_length=70000)
    comment_selection = models.ForeignKey(CommentSelection, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.text


class CommentSelectionRepository:
    @staticmethod
    def load_comment_selection(question: Question, model_method: str):
        db_comment_selection = CommentSelection.objects.get(question_id=question.id, recommendation_method=model_method)
        comments = Comment.objects.filter(comment_selection_id=db_comment_selection.id)
        domain_comments = [Comment(comment.id, remove_html_tags(comment.text)) for comment in comments]

        random.shuffle(domain_comments)

        return DomainCommentSuggestion(db_comment_selection.id, recommendation_method=db_comment_selection.recommendation_method, comments=domain_comments)
