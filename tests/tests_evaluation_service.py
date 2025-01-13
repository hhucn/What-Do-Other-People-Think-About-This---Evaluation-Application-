import unittest
from unittest.mock import Mock

from evaluation.applicationservice.EvaluationService import EvaluationService
from evaluation.domain.Participant import Participant
from evaluation.domain.Participant import Participant as DomainParticipant
from evaluation.domain.PointOfViewQuestion import PointOfViewQuestion
from evaluation.models.ParticipantRepository import ParticipantRepository
from evaluation.models.QuestionRepository import QuestionRepository


def create_question_repository_mock():
    question_repository = Mock(QuestionRepository)
    questions = [PointOfViewQuestion(question_id=1, comment_selections=None, user_comment="", article_keywords="", article_title="bar", news_agency="foo"),
                 PointOfViewQuestion(question_id=2, comment_selections=None, user_comment="", article_keywords="", article_title="bar", news_agency="foo"),
                 PointOfViewQuestion(question_id=3, comment_selections=None, user_comment="", article_keywords="", article_title="bar", news_agency="foo"),
                 PointOfViewQuestion(question_id=4, comment_selections=None, user_comment="", article_keywords="", article_title="bar", news_agency="foo"), ]
    question_repository.get_questions.return_value = questions
    return question_repository, questions


def create_participant_repository_mock():
    participant_repository = Mock(ParticipantRepository)
    participant = Participant(1, "Charlie", [], next_question=None, progress=0)
    return participant, participant_repository


class EvaluationServiceTests(unittest.TestCase):

    def test_get_participant_that_has_not_been_loaded(self):
        participant, participant_repository = create_participant_repository_mock()
        participant_repository.load_participant.return_value = participant
        evaluation_service = EvaluationService(None, None, participant_repository)

        loaded_participant = evaluation_service.get_participant(1)

        self.assertEqual(loaded_participant, participant)

    def test_get_participant_when_participant_does_not_exists(self):
        participant_repository = Mock(ParticipantRepository)
        participant_repository.load_participant.return_value = None
        evaluation_service = EvaluationService(None, None, participant_repository)

        loaded_participant = evaluation_service.get_participant(42)

        self.assertIsNone(loaded_participant)

    def test_get_participant_with_next_question_new_question(self):
        participant, participant_repository = create_participant_repository_mock()
        evaluation_service = EvaluationService(None, None, participant_repository)
        evaluation_service.get_participant_with_next_question(1, None, None)

        participant_repository.load_participant_with_next_question.assert_called_with(1)

    def test_get_participant_with_next_question_question_started(self):
        participant, participant_repository = create_participant_repository_mock()
        evaluation_service = EvaluationService(None, None, participant_repository)
        evaluation_service.get_participant_with_next_question(1, 1, "stance")

        participant_repository.load_participant_with_next_comment_question(1, 1, "stance")

    def test_get_participant_with_next_question_all_comment_questions_answered(self):
        participant, participant_repository = create_participant_repository_mock()
        participant_repository.load_participant_with_next_comment_question.return_value = DomainParticipant(participant_id=1, user_name="Groot",
                                                                                                            processed_questions=[], progress=0.0, next_question=None)
        evaluation_service = EvaluationService(None, None, participant_repository)
        evaluation_service.get_participant_with_next_question(1, 1, "stance")

        participant_repository.load_participant_with_point_of_view_question.assert_called_with(1, 1, "stance")


if __name__ == '__main__':
    unittest.main()
