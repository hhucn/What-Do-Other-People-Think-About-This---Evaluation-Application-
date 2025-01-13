import unittest

from django.db import IntegrityError

from evaluation.models import CommentSelection, Comment
from evaluation.models.AnswerRepository import AnswerRepository
from evaluation.models.AnswerRepository import PointOfViewSetAnswer as DbAnswer, CommentAnswer
from evaluation.models.Participant import Participant as DBParticipant
from evaluation.models.Questions import Question as DBQuestion


class AnswerRepositoryTests(unittest.TestCase):

    def setUp(self):
        self.participant_1 = DBParticipant.objects.create_user(username="Bob")
        self.participant_2 = DBParticipant.objects.create_user(username="Alice")
        self.participant_3 = DBParticipant.objects.create_user(username="Charlie")
        self.participant_4 = DBParticipant.objects.create_user(username="Charlies Dog")
        self.question_1 = DBQuestion.objects.create(user_comment="I am a test comment 1")
        self.question_2 = DBQuestion.objects.create(user_comment="I am a test comment 2")
        self.question_3 = DBQuestion.objects.create(user_comment="I am a test comment 3")
        self.question_4 = DBQuestion.objects.create(user_comment="I am a test comment 4")
        self.question_5 = DBQuestion.objects.create(user_comment="I am a test comment 5")
        self.question_6 = DBQuestion.objects.create(user_comment="I am a test comment 6")

        self.participant_1.questions.add(self.question_1)
        self.participant_1.questions.add(self.question_2)
        self.participant_1.questions.add(self.question_3)
        self.participant_2.questions.add(self.question_4)
        self.participant_2.questions.add(self.question_5)
        self.participant_2.questions.add(self.question_6)

        self.comment_selection_1 = CommentSelection.objects.create(question=self.question_1, recommendation_method="stance")
        self.comment_selection_2 = CommentSelection.objects.create(question=self.question_1, recommendation_method="news-agency")

        self.comment_1 = Comment.objects.create(comment_selection=self.comment_selection_1, text="I am a test comment 1")

    def tearDown(self):
        DBQuestion.objects.all().delete()
        DBParticipant.objects.all().delete()
        DbAnswer.objects.all().delete()
        CommentAnswer.objects.all().delete()

    def test_save_point_of_view_set_answer(self):
        db_answers = DbAnswer.objects.all()
        self.assertEqual(len(db_answers), 0)

        AnswerRepository.save_point_of_view_set_answer(participant_id=self.participant_1.id, question_id=self.question_1.id, recommendation_method="stance", selected_method="random")

        db_answers = DbAnswer.objects.all()
        self.assertEqual(len(db_answers), 1)

    def test_do_not_save_duplicate_save_point_of_view_set_answer(self):
        with self.assertRaises(IntegrityError):
            AnswerRepository.save_point_of_view_set_answer(participant_id=self.participant_1.id, question_id=self.question_1.id, recommendation_method="stance", selected_method="random")
            AnswerRepository.save_point_of_view_set_answer(participant_id=self.participant_1.id, question_id=self.question_1.id, recommendation_method="stance", selected_method="random")

    def test_save_random_as_selected_answers_does_not_trigger_duplicate_answers(self):
        AnswerRepository.save_point_of_view_set_answer(participant_id=self.participant_1.id, question_id=self.question_1.id, recommendation_method="random", selected_method="stance")
        AnswerRepository.save_point_of_view_set_answer(participant_id=self.participant_1.id, question_id=self.question_1.id, recommendation_method="random", selected_method="sentiment")

        db_answers = DbAnswer.objects.all()
        self.assertEqual(len(db_answers), 2)

    def test_save_comment_answer(self):
        db_comment_answers = CommentAnswer.objects.all()
        self.assertEqual(len(db_comment_answers), 0)

        AnswerRepository.save_comment_answer(participant_id=self.participant_1.id, question_id=self.question_1.id,
                                             comment_id=self.comment_1.id, good_recommendation=True)

        db_comment_answers = CommentAnswer.objects.all()
        self.assertEqual(len(db_comment_answers), 1)
        self.assertEqual(db_comment_answers[0].participant, self.participant_1)
        self.assertEqual(db_comment_answers[0].question, self.question_1)
        self.assertEqual(db_comment_answers[0].comment, self.comment_1)
        self.assertEqual(db_comment_answers[0].comment_selection, self.comment_selection_1)
        self.assertEqual(db_comment_answers[0].good_recommendation, True)

    def test_do_not_save_duplicate_comment_answer(self):
        with self.assertRaises(IntegrityError):
            AnswerRepository.save_comment_answer(participant_id=self.participant_1.id, question_id=self.question_1.id,
                                                 comment_id=self.comment_1.id, good_recommendation=True)
            AnswerRepository.save_comment_answer(participant_id=self.participant_1.id, question_id=self.question_1.id,
                                                 comment_id=self.comment_1.id, good_recommendation=False)


if __name__ == '__main__':
    unittest.main()
