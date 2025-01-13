import unittest

from evaluation.models import Question, CommentSelection, Comment
from evaluation.models.CommentRepository import CommentSelectionRepository


class TestCommentRepository(unittest.TestCase):

    def setUp(self):
        self.question = Question.objects.create(user_comment="I am a test comment", article_keywords="Foo Bar")
        self.comment_selection = CommentSelection.objects.create(question_id=self.question.id, recommendation_method="stance")
        comment_1 = Comment.objects.create(comment_selection_id=self.comment_selection.id, text="I am a test comment")
        comment_2 = Comment.objects.create(comment_selection_id=self.comment_selection.id, text="I am a test comment")
        comment_3 = Comment.objects.create(comment_selection_id=self.comment_selection.id, text="I am a test comment")

    def tearDown(self):
        Question.objects.all().delete()
        CommentSelection.objects.all().delete()
        Comment.objects.all().delete()

    def test_load_comment_selection(self):
        selection = CommentSelectionRepository.load_comment_selection(self.question, "stance")
        self.assertEqual(selection.id, self.comment_selection.id)  # add assertion here


if __name__ == '__main__':
    unittest.main()
