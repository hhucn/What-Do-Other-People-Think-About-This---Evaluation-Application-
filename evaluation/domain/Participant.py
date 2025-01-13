from typing import List

from evaluation.domain.PointOfViewQuestion import PointOfViewQuestion


class Participant:
    def __init__(self, participant_id: int, user_name: str, processed_questions: List[PointOfViewQuestion], next_question: PointOfViewQuestion, progress):
        self.id = participant_id
        self.user_name = user_name
        self.processed_questions = processed_questions
        self.next_question = next_question
        self.progress = progress

    def get_progress(self) -> int:
        return self.progress

    def get_id(self) -> int:
        return self.id

    def get_user_name(self):
        return self.user_name

    def get_processed_questions(self) -> List[PointOfViewQuestion]:
        return self.processed_questions

    def add_processed_question(self, question):
        if question in self.processed_questions:
            raise QuestionAlreadyProcessedError("Question has already been answered by the participant")
        self.processed_questions.append(question)

    def get_next_question(self):
        return self.next_question


class QuestionAlreadyProcessedError(Exception):
    pass
