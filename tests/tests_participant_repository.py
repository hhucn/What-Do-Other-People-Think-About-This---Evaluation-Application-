import random
import unittest
from unittest.mock import patch

from django.core.exceptions import ObjectDoesNotExist

from evaluation.domain.DomainCommentQuestion import DomainCommentQuestion
from evaluation.models import Question, PointOfViewSetAnswer, CommentSelection, Comment
from evaluation.models.Participant import Participant
from evaluation.models.ParticipantRepository import ParticipantRepository


class ParticipantRepositoryTest(unittest.TestCase):

    def setUp(self):
        random.seed(1)

        self.participant_1 = Participant.objects.create_user(username="Alice")

        self.question_1 = Question.objects.create(user_comment="I am a user comment 1", article_keywords="Keyword 1, Keyword 2")
        self.question_2 = Question.objects.create(user_comment="I am a user comment 2", article_keywords="Keyword 1, Keyword 3")
        self.question_3 = Question.objects.create(user_comment="I am a user comment 3", article_keywords="Keyword 4, Keyword 1")
        self.question_4 = Question.objects.create(user_comment="I am a user comment 4", article_keywords="Keyword 5, Keyword 6")

        self.participant_1.questions.add(self.question_1)
        self.participant_1.questions.add(self.question_2)
        self.participant_1.questions.add(self.question_3)
        self.participant_1.questions.add(self.question_4)

        self.comment_selection_1 = CommentSelection.objects.create(question=self.question_1, recommendation_method="news-agency")
        self.comment_selection_2 = CommentSelection.objects.create(question=self.question_2, recommendation_method="news-agency")
        self.comment_selection_3 = CommentSelection.objects.create(question=self.question_3, recommendation_method="news-agency")
        self.comment_selection_4 = CommentSelection.objects.create(question=self.question_4, recommendation_method="news-agency")

        self.comment_selection_5 = CommentSelection.objects.create(question=self.question_1, recommendation_method="sentiment")
        self.comment_selection_6 = CommentSelection.objects.create(question=self.question_2, recommendation_method="sentiment")
        self.comment_selection_7 = CommentSelection.objects.create(question=self.question_3, recommendation_method="sentiment")
        self.comment_selection_8 = CommentSelection.objects.create(question=self.question_4, recommendation_method="sentiment")

        self.comment_selection_9 = CommentSelection.objects.create(question=self.question_1, recommendation_method="emotion")
        self.comment_selection_10 = CommentSelection.objects.create(question=self.question_2, recommendation_method="emotion")
        self.comment_selection_11 = CommentSelection.objects.create(question=self.question_3, recommendation_method="emotion")
        self.comment_selection_12 = CommentSelection.objects.create(question=self.question_4, recommendation_method="emotion")

        self.comment_selection_13 = CommentSelection.objects.create(question=self.question_1, recommendation_method="random")
        self.comment_selection_14 = CommentSelection.objects.create(question=self.question_2, recommendation_method="random")
        self.comment_selection_15 = CommentSelection.objects.create(question=self.question_3, recommendation_method="random")
        self.comment_selection_16 = CommentSelection.objects.create(question=self.question_4, recommendation_method="random")

        self.comment_selection_17 = CommentSelection.objects.create(question=self.question_1, recommendation_method="stance")
        self.comment_selection_18 = CommentSelection.objects.create(question=self.question_2, recommendation_method="stance")
        self.comment_selection_19 = CommentSelection.objects.create(question=self.question_3, recommendation_method="stance")
        self.comment_selection_20 = CommentSelection.objects.create(question=self.question_4, recommendation_method="stance")

        self.comment_1 = Comment.objects.create(text="I am a test comment 1", comment_selection=self.comment_selection_1)
        self.comment_2 = Comment.objects.create(text="I am a test comment 2", comment_selection=self.comment_selection_1)
        self.comment_3 = Comment.objects.create(text="I am a test comment 3", comment_selection=self.comment_selection_1)
        self.comment_4 = Comment.objects.create(text="I am a test comment 4", comment_selection=self.comment_selection_1)

        self.comment_5 = Comment.objects.create(text="I am a test comment 5", comment_selection=self.comment_selection_5)
        self.comment_6 = Comment.objects.create(text="I am a test comment 6", comment_selection=self.comment_selection_5)
        self.comment_7 = Comment.objects.create(text="I am a test comment 7", comment_selection=self.comment_selection_5)
        self.comment_8 = Comment.objects.create(text="I am a test comment 8", comment_selection=self.comment_selection_5)

        self.comment_9 = Comment.objects.create(text="I am a test comment 9", comment_selection=self.comment_selection_9)
        self.comment_10 = Comment.objects.create(text="I am a test comment 10", comment_selection=self.comment_selection_9)
        self.comment_11 = Comment.objects.create(text="I am a test comment 11", comment_selection=self.comment_selection_9)
        self.comment_12 = Comment.objects.create(text="I am a test comment 12", comment_selection=self.comment_selection_9)

        self.comment_13 = Comment.objects.create(text="I am a test comment 13", comment_selection=self.comment_selection_13)
        self.comment_14 = Comment.objects.create(text="I am a test comment 14", comment_selection=self.comment_selection_13)
        self.comment_15 = Comment.objects.create(text="I am a test comment 15", comment_selection=self.comment_selection_13)
        self.comment_16 = Comment.objects.create(text="I am a test comment 16", comment_selection=self.comment_selection_13)

        self.comment_13 = Comment.objects.create(text="I am a test comment 17", comment_selection=self.comment_selection_17)
        self.comment_14 = Comment.objects.create(text="I am a test comment 18", comment_selection=self.comment_selection_17)
        self.comment_15 = Comment.objects.create(text="I am a test comment 19", comment_selection=self.comment_selection_17)
        self.comment_16 = Comment.objects.create(text="I am a test comment 20", comment_selection=self.comment_selection_17)

    def tearDown(self):
        Participant.objects.all().delete()
        Question.objects.all().delete()
        PointOfViewSetAnswer.objects.all().delete()
        CommentSelection.objects.all().delete()

    def test_load_participant_no_questions_answered_yet(self):
        loaded_participant = ParticipantRepository.load_participant(self.participant_1.id)

        self.assertEqual(loaded_participant.get_user_name(), "Alice")

        self.assertListEqual(loaded_participant.get_processed_questions(), [])

    def test_load_participant_some_questions_answered(self):
        PointOfViewSetAnswer.objects.create(question=self.question_1, participant=self.participant_1, recommendation_method="stance")
        PointOfViewSetAnswer.objects.create(question=self.question_2, participant=self.participant_1, recommendation_method="stance")

        loaded_participant = ParticipantRepository.load_participant(self.participant_1.id)
        loaded_participant_processed_questions = [question.user_comment for question in loaded_participant.get_processed_questions()]

        self.assertEqual(len(loaded_participant_processed_questions), 2)
        self.assertIn(self.question_1.user_comment, loaded_participant_processed_questions)
        self.assertIn(self.question_2.user_comment, loaded_participant_processed_questions)

    def test_load_participant_if_participant_does_not_exist(self):
        with self.assertRaises(ObjectDoesNotExist):
            ParticipantRepository.load_participant(2)

    def test_set_next_question_for_participant(self):
        PointOfViewSetAnswer.objects.create(question=self.question_1, participant=self.participant_1, recommendation_method="news-agency")
        PointOfViewSetAnswer.objects.create(question=self.question_1, participant=self.participant_1, recommendation_method="sentiment")
        PointOfViewSetAnswer.objects.create(question=self.question_1, participant=self.participant_1, recommendation_method="emotion")
        PointOfViewSetAnswer.objects.create(question=self.question_1, participant=self.participant_1, recommendation_method="stance")

        PointOfViewSetAnswer.objects.create(question=self.question_2, participant=self.participant_1, recommendation_method="news-agency")
        PointOfViewSetAnswer.objects.create(question=self.question_2, participant=self.participant_1, recommendation_method="sentiment")
        PointOfViewSetAnswer.objects.create(question=self.question_2, participant=self.participant_1, recommendation_method="emotion")
        PointOfViewSetAnswer.objects.create(question=self.question_2, participant=self.participant_1, recommendation_method="stance")

        loaded_participant = ParticipantRepository.load_participant(self.participant_1.id)

        self.assertEqual(loaded_participant.get_next_question().user_comment, self.question_4.user_comment)

    def test_next_question_for_participant_is_none_if_all_questions_answered(self):
        PointOfViewSetAnswer.objects.create(question=self.question_1, participant=self.participant_1, recommendation_method="news-agency")
        PointOfViewSetAnswer.objects.create(question=self.question_2, participant=self.participant_1, recommendation_method="news-agency")
        PointOfViewSetAnswer.objects.create(question=self.question_3, participant=self.participant_1, recommendation_method="news-agency")
        PointOfViewSetAnswer.objects.create(question=self.question_4, participant=self.participant_1, recommendation_method="news-agency")

        PointOfViewSetAnswer.objects.create(question=self.question_1, participant=self.participant_1, recommendation_method="stance")
        PointOfViewSetAnswer.objects.create(question=self.question_2, participant=self.participant_1, recommendation_method="stance")
        PointOfViewSetAnswer.objects.create(question=self.question_3, participant=self.participant_1, recommendation_method="stance")
        PointOfViewSetAnswer.objects.create(question=self.question_4, participant=self.participant_1, recommendation_method="stance")

        PointOfViewSetAnswer.objects.create(question=self.question_1, participant=self.participant_1, recommendation_method="emotion")
        PointOfViewSetAnswer.objects.create(question=self.question_2, participant=self.participant_1, recommendation_method="emotion")
        PointOfViewSetAnswer.objects.create(question=self.question_3, participant=self.participant_1, recommendation_method="emotion")
        PointOfViewSetAnswer.objects.create(question=self.question_4, participant=self.participant_1, recommendation_method="emotion")

        PointOfViewSetAnswer.objects.create(question=self.question_1, participant=self.participant_1, recommendation_method="sentiment")
        PointOfViewSetAnswer.objects.create(question=self.question_2, participant=self.participant_1, recommendation_method="sentiment")
        PointOfViewSetAnswer.objects.create(question=self.question_3, participant=self.participant_1, recommendation_method="sentiment")
        PointOfViewSetAnswer.objects.create(question=self.question_4, participant=self.participant_1, recommendation_method="sentiment")
        participant = ParticipantRepository.load_participant(self.participant_1.id)

        self.assertIsNone(participant.get_next_question())

    def test_load_participant_with_next_question(self):
        with patch("evaluation.models.ParticipantRepository.QuestionRepository.get_next_question") as get_next_question_mock:
            get_next_question_mock.return_value = DomainCommentQuestion(question=self.question_1, comment_selection=self.comment_selection_1, comment=self.comment_1, recommendation_method="stance")
            participant = ParticipantRepository.load_participant_with_next_question(participant_id=self.participant_1.id)

            get_next_question_mock.assert_called_once()

            self.assertEqual(participant.user_name, self.participant_1.username)

    def test_load_participant_with_next_comment_question(self):
        with patch("evaluation.models.ParticipantRepository.QuestionRepository.get_comment_question") as get_next_question_mock:
            participant = ParticipantRepository.load_participant_with_next_comment_question(participant_id=self.participant_1.id, question_id=self.question_1.id,
                                                                                            recommendation_method="sentiment")

            get_next_question_mock.assert_called_once()

            self.assertEqual(participant.user_name, self.participant_1.username)

    def test_load_participant_with_point_of_view_question(self):
        with patch('evaluation.models.ParticipantRepository.QuestionRepository.get_point_of_view_question') as get_next_question_mock:
            participant = ParticipantRepository.load_participant_with_point_of_view_question(participant_id=self.participant_1.id, question_id=self.question_1.id,
                                                                                             recommendation_method="sentiment")

            get_next_question_mock.assert_called_once()
            self.assertEqual(participant.user_name, self.participant_1.username)


if __name__ == '__main__':
    unittest.main()
