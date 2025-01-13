import os
import random
import unittest

import django

from evaluation.domain.DomainCommentQuestion import DomainCommentQuestion
from evaluation.models import Question, CommentSelection, Comment
from evaluation.models.AnswerRepository import CommentAnswer
from evaluation.models.Participant import Participant as DBParticipant, Participant
from evaluation.models.QuestionRepository import QuestionRepository

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evaluationApplication.settings')
django.setup()


class QuestionRepositoryCase(unittest.TestCase):
    def setUp(self):
        random.seed(1)

        # TODO: Refactor db setup in util file for other tests
        self.participant_1 = DBParticipant.objects.create_user(username="Bob")
        self.participant_2 = DBParticipant.objects.create_user(username="Alice")
        self.participant_3 = DBParticipant.objects.create_user(username="Charlie")
        self.participant_4 = DBParticipant.objects.create_user(username="Charlies Dog")
        self.question_1 = Question.objects.create(user_comment="I am a test comment 1")
        self.question_2 = Question.objects.create(user_comment="I am a test comment 2")
        self.question_3 = Question.objects.create(user_comment="I am a test comment 3")

        self.participant_1.questions.add(self.question_1)
        self.participant_1.questions.add(self.question_2)
        self.participant_1.questions.add(self.question_3)

        self.comment_selection_1 = CommentSelection.objects.create(recommendation_method="news-agency", question_id=self.question_1.id)
        self.comment_selection_2 = CommentSelection.objects.create(recommendation_method="news-agency", question_id=self.question_2.id)
        self.comment_selection_3 = CommentSelection.objects.create(recommendation_method="news-agency", question_id=self.question_3.id)

        self.comment_selection_4 = CommentSelection.objects.create(recommendation_method="stance", question_id=self.question_1.id)
        self.comment_selection_5 = CommentSelection.objects.create(recommendation_method="stance", question_id=self.question_2.id)
        self.comment_selection_6 = CommentSelection.objects.create(recommendation_method="stance", question_id=self.question_3.id)

        self.comment_selection_7 = CommentSelection.objects.create(recommendation_method="sentiment", question_id=self.question_1.id)
        self.comment_selection_8 = CommentSelection.objects.create(recommendation_method="sentiment", question_id=self.question_2.id)
        self.comment_selection_9 = CommentSelection.objects.create(recommendation_method="sentiment", question_id=self.question_3.id)

        self.comment_selection_10 = CommentSelection.objects.create(recommendation_method="emotion", question_id=self.question_1.id)
        self.comment_selection_11 = CommentSelection.objects.create(recommendation_method="emotion", question_id=self.question_2.id)
        self.comment_selection_12 = CommentSelection.objects.create(recommendation_method="emotion", question_id=self.question_3.id)

        self.comment_selection_13 = CommentSelection.objects.create(recommendation_method="random", question_id=self.question_1.id)
        self.comment_selection_14 = CommentSelection.objects.create(recommendation_method="random", question_id=self.question_2.id)
        self.comment_selection_15 = CommentSelection.objects.create(recommendation_method="random", question_id=self.question_3.id)

        self.comment_1 = Comment.objects.create(text="I am a test comment 1", comment_selection=self.comment_selection_3)
        self.comment_2 = Comment.objects.create(text="I am a test comment 2", comment_selection=self.comment_selection_3)
        self.comment_3 = Comment.objects.create(text="I am a test comment 3", comment_selection=self.comment_selection_3)
        self.comment_4 = Comment.objects.create(text="I am a test comment 4", comment_selection=self.comment_selection_3)

        self.comment_5 = Comment.objects.create(text="I am a test comment 5", comment_selection=self.comment_selection_6)
        self.comment_6 = Comment.objects.create(text="I am a test comment 6", comment_selection=self.comment_selection_6)
        self.comment_7 = Comment.objects.create(text="I am a test comment 7", comment_selection=self.comment_selection_6)
        self.comment_8 = Comment.objects.create(text="I am a test comment 8", comment_selection=self.comment_selection_6)

        self.comment_9 = Comment.objects.create(text="I am a test comment 9", comment_selection=self.comment_selection_9)
        self.comment_10 = Comment.objects.create(text="I am a test comment 10", comment_selection=self.comment_selection_9)
        self.comment_11 = Comment.objects.create(text="I am a test comment 11", comment_selection=self.comment_selection_9)
        self.comment_12 = Comment.objects.create(text="I am a test comment 12", comment_selection=self.comment_selection_9)

        self.comment_13 = Comment.objects.create(text="I am a test comment 13", comment_selection=self.comment_selection_12)
        self.comment_14 = Comment.objects.create(text="I am a test comment 14", comment_selection=self.comment_selection_12)
        self.comment_15 = Comment.objects.create(text="I am a test comment 15", comment_selection=self.comment_selection_12)
        self.comment_16 = Comment.objects.create(text="I am a test comment 16", comment_selection=self.comment_selection_12)

        self.comment_13 = Comment.objects.create(text="I am a test comment 17", comment_selection=self.comment_selection_15)
        self.comment_14 = Comment.objects.create(text="I am a test comment 18", comment_selection=self.comment_selection_15)
        self.comment_15 = Comment.objects.create(text="I am a test comment 19", comment_selection=self.comment_selection_15)
        self.comment_16 = Comment.objects.create(text="I am a test comment 20", comment_selection=self.comment_selection_15)

        self.comment_1 = Comment.objects.create(text="I am a test comment 1", comment_selection=self.comment_selection_2)
        self.comment_2 = Comment.objects.create(text="I am a test comment 2", comment_selection=self.comment_selection_2)
        self.comment_3 = Comment.objects.create(text="I am a test comment 3", comment_selection=self.comment_selection_2)
        self.comment_4 = Comment.objects.create(text="I am a test comment 4", comment_selection=self.comment_selection_2)

        self.comment_5 = Comment.objects.create(text="I am a test comment 5", comment_selection=self.comment_selection_8)
        self.comment_6 = Comment.objects.create(text="I am a test comment 6", comment_selection=self.comment_selection_8)
        self.comment_7 = Comment.objects.create(text="I am a test comment 7", comment_selection=self.comment_selection_8)
        self.comment_8 = Comment.objects.create(text="I am a test comment 8", comment_selection=self.comment_selection_8)

        self.comment_9 = Comment.objects.create(text="I am a test comment 9", comment_selection=self.comment_selection_11)
        self.comment_10 = Comment.objects.create(text="I am a test comment 10", comment_selection=self.comment_selection_11)
        self.comment_11 = Comment.objects.create(text="I am a test comment 11", comment_selection=self.comment_selection_11)
        self.comment_12 = Comment.objects.create(text="I am a test comment 12", comment_selection=self.comment_selection_11)

        self.comment_13 = Comment.objects.create(text="I am a test comment 13", comment_selection=self.comment_selection_14)
        self.comment_14 = Comment.objects.create(text="I am a test comment 14", comment_selection=self.comment_selection_14)
        self.comment_15 = Comment.objects.create(text="I am a test comment 15", comment_selection=self.comment_selection_14)
        self.comment_16 = Comment.objects.create(text="I am a test comment 16", comment_selection=self.comment_selection_14)

        self.comment_13 = Comment.objects.create(text="I am a test comment 17", comment_selection=self.comment_selection_5)
        self.comment_14 = Comment.objects.create(text="I am a test comment 18", comment_selection=self.comment_selection_5)
        self.comment_15 = Comment.objects.create(text="I am a test comment 19", comment_selection=self.comment_selection_5)
        self.comment_16 = Comment.objects.create(text="I am a test comment 20", comment_selection=self.comment_selection_5)

        self.comment_1 = Comment.objects.create(text="I am a test comment 1", comment_selection=self.comment_selection_1)
        self.comment_2 = Comment.objects.create(text="I am a test comment 2", comment_selection=self.comment_selection_1)
        self.comment_3 = Comment.objects.create(text="I am a test comment 3", comment_selection=self.comment_selection_1)
        self.comment_4 = Comment.objects.create(text="I am a test comment 4", comment_selection=self.comment_selection_1)

        self.comment_5 = Comment.objects.create(text="I am a test comment 5", comment_selection=self.comment_selection_13)
        self.comment_6 = Comment.objects.create(text="I am a test comment 6", comment_selection=self.comment_selection_13)
        self.comment_7 = Comment.objects.create(text="I am a test comment 7", comment_selection=self.comment_selection_13)
        self.comment_8 = Comment.objects.create(text="I am a test comment 8", comment_selection=self.comment_selection_13)

        self.comment_9 = Comment.objects.create(text="I am a test comment 9", comment_selection=self.comment_selection_7)
        self.comment_10 = Comment.objects.create(text="I am a test comment 10", comment_selection=self.comment_selection_7)
        self.comment_11 = Comment.objects.create(text="I am a test comment 11", comment_selection=self.comment_selection_7)
        self.comment_12 = Comment.objects.create(text="I am a test comment 12", comment_selection=self.comment_selection_7)

        self.comment_13 = Comment.objects.create(text="I am a test comment 13", comment_selection=self.comment_selection_10)
        self.comment_14 = Comment.objects.create(text="I am a test comment 14", comment_selection=self.comment_selection_10)
        self.comment_15 = Comment.objects.create(text="I am a test comment 15", comment_selection=self.comment_selection_10)
        self.comment_16 = Comment.objects.create(text="I am a test comment 16", comment_selection=self.comment_selection_10)

        self.comment_13 = Comment.objects.create(text="I am a test comment 17", comment_selection=self.comment_selection_4)
        self.comment_14 = Comment.objects.create(text="I am a test comment 18", comment_selection=self.comment_selection_4)
        self.comment_15 = Comment.objects.create(text="I am a test comment 19", comment_selection=self.comment_selection_4)
        self.comment_16 = Comment.objects.create(text="I am a test comment 20", comment_selection=self.comment_selection_4)

    def tearDown(self):
        Participant.objects.all().delete()
        Question.objects.all().delete()
        CommentSelection.objects.all().delete()
        Comment.objects.all().delete()
        CommentAnswer.objects.all().delete()

    def test_get_questions(self):
        questions = QuestionRepository.get_point_of_view_questions()

        self.assertEqual(len(questions), 12)

    def test_get_questions_contains_random_and_method_comment_selection(self):
        questions = QuestionRepository.get_point_of_view_questions()

        comment_selection_first_element = [question.comment_selections[0].recommendation_method for question in questions]
        comment_selection_second_element = [question.comment_selections[1].recommendation_method for question in questions]

        self.assertNotEqual(len(set(comment_selection_first_element)), 1)
        self.assertNotEqual(len(set(comment_selection_second_element)), 1)

    def test_get_comment_question(self):
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_4,
                                     comment=self.comment_1, good_recommendation=True)

        question = QuestionRepository.get_comment_question(participant_id=self.participant_1.id, question_id=self.question_1.id,
                                                           recommendation_method="stance")

        expected_comments = [self.comment_5.text, self.comment_6.text, self.comment_7.text, self.comment_8.text]

        self.assertEqual(question.question, self.question_1)
        self.assertIn(question.comment.text, expected_comments)

    def test_get_comment_question_all_answered_but_one(self):
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_4, comment=self.comment_1, good_recommendation=False)
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_4, comment=self.comment_2, good_recommendation=False)
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_4, comment=self.comment_3, good_recommendation=False)
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_4, comment=self.comment_4, good_recommendation=False)
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_13, comment=self.comment_5, good_recommendation=False)
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_13, comment=self.comment_6, good_recommendation=False)
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_13, comment=self.comment_7, good_recommendation=False)

        question = QuestionRepository.get_comment_question(participant_id=self.participant_1.id, question_id=self.question_1.id, recommendation_method="stance")

        self.assertEqual(question.question, self.question_1)
        self.assertEqual(question.comment.text, self.comment_14.text)

    def test_get_comment_question_all_answered(self):
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_4, comment=self.comment_1, good_recommendation=False)
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_4, comment=self.comment_2, good_recommendation=False)
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_4, comment=self.comment_3, good_recommendation=False)
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_4, comment=self.comment_4, good_recommendation=True)
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_13, comment=self.comment_5, good_recommendation=False)
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_13, comment=self.comment_6, good_recommendation=True)
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_13, comment=self.comment_7, good_recommendation=False)
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_13, comment=self.comment_8, good_recommendation=False)
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_7, comment=self.comment_9, good_recommendation=False)
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_7, comment=self.comment_10, good_recommendation=False)
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_7, comment=self.comment_11, good_recommendation=False)
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_7, comment=self.comment_12, good_recommendation=True)
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_10, comment=self.comment_13, good_recommendation=False)
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_10, comment=self.comment_14, good_recommendation=True)
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_10, comment=self.comment_15, good_recommendation=False)
        CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.comment_selection_10, comment=self.comment_16, good_recommendation=False)

        question = QuestionRepository.get_comment_question(participant_id=self.participant_1.id, question_id=self.question_1.id, recommendation_method="stance")

        self.assertIsNone(question)

    def test_get_next_question_no_question_answered(self):
        random.seed(5)
        question: DomainCommentQuestion = QuestionRepository.get_next_question(self.participant_1.id)

        self.assertEqual(question.question, self.question_2)
        self.assertEqual(question.comment_selection.recommendation_method, self.comment_selection_11.recommendation_method)
        self.assertEqual(question.comment.text, self.comment_11.text)

    def test_get_point_of_view_question(self):
        question = QuestionRepository.get_point_of_view_question(question_id=self.question_1.id, recommendation_method="stance")

        comments = question.comment_selections[0].get_comments()
        comments.extend(question.comment_selections[1].get_comments())

        self.assertEqual(question.user_comment, self.question_1.user_comment)
        self.assertEqual(question.recommendation_method, self.comment_selection_4.recommendation_method)
        self.assertIn(self.comment_13, comments)
        self.assertIn(self.comment_14, comments)
        self.assertIn(self.comment_15, comments)
        self.assertIn(self.comment_16, comments)
        self.assertIn(self.comment_5, comments)
        self.assertIn(self.comment_6, comments)
        self.assertIn(self.comment_7, comments)
        self.assertIn(self.comment_8, comments)


if __name__ == '__main__':
    unittest.main()
