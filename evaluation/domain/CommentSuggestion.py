from typing import List

from evaluation.domain.Comment import Comment


class CommentSuggestion:
    def __init__(self, comment_suggestion_id: int, recommendation_method: str, comments: List[Comment]):
        self.id = comment_suggestion_id
        self.recommendation_method = recommendation_method
        self.comments = comments

    def get_suggestion_name(self):
        return self.recommendation_method

    def get_comments(self):
        return self.comments

    def get_id(self):
        return self.id
