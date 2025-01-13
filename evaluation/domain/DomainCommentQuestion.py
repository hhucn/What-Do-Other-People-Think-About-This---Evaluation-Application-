from evaluation.models import Question, Comment, CommentSelection


class DomainCommentQuestion:
    def __init__(self, question: Question, comment_selection: CommentSelection, comment: Comment, recommendation_method: str):
        self.question = question
        self.comment_selection = comment_selection
        self.comment = comment
        self.recommendation_method = recommendation_method
