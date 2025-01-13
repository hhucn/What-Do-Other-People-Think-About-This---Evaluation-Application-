from typing import List, Mapping

from evaluation.domain.Participant import Participant
from evaluation.domain.PointOfViewQuestion import PointOfViewQuestion
from evaluation.models.AnswerRepository import AnswerRepository
from evaluation.models.ParticipantRepository import ParticipantRepository
from evaluation.models.QuestionRepository import QuestionRepository


class AllQuestionsAnsweredError(Exception):
    pass


class EvaluationService:

    def __init__(self, question_repository: QuestionRepository, answer_repository: AnswerRepository, participant_repository: ParticipantRepository):
        self.participants: Mapping[int, Participant] = {}
        self.question_repository = question_repository
        self.answer_repository = answer_repository
        self.participant_repository = participant_repository
        self.questions: Mapping[int, List[PointOfViewQuestion]] = {}

    def save_point_of_view_answer(self, participant_id: int, question_id: int, recommendation_method: str, selected_method: str) -> None:
        self.answer_repository.save_point_of_view_set_answer(participant_id, question_id, recommendation_method, selected_method)

    def get_participant(self, participant_id: int) -> Participant:
        return self.participant_repository.load_participant(participant_id)

    def get_participant_with_next_question(self, participant_id: int, question_id=None, recommendation_method: str = None) -> Participant:
        if question_id is None:
            print(f"Load new question")
            participant = self.participant_repository.load_participant_with_next_question(participant_id)
        else:
            print(f"Load next comment question")
            participant = self.participant_repository.load_participant_with_next_comment_question(participant_id, question_id, recommendation_method)

            if participant.get_next_question() is None:
                print("Load point of view question")
                participant = self.participant_repository.load_participant_with_point_of_view_question(participant_id, question_id, recommendation_method)

        return participant

    def save_comment_answer(self, participant_id, question_id, recommendation_method, comment_id, good_recommendation):
        self.answer_repository.save_comment_answer(participant_id=participant_id, question_id=question_id,
                                                   comment_id=comment_id, good_recommendation=good_recommendation)
        return self.participant_repository.load_participant_with_next_comment_question(participant_id, question_id, recommendation_method)
