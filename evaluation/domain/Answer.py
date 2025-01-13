from evaluation.domain.Participant import Participant
from evaluation.domain.PointOfViewQuestion import PointOfViewQuestion


class Answer:
    def __init__(self, answer_id: int, question: PointOfViewQuestion, participant: Participant, answer: int):
        self.id = answer_id
        self.question = question
        self.participant = participant
        self.answer = answer

    def get_question(self):
        return self.question

    def get_answer(self):
        return self.answer

    def get_participant(self):
        return self.participant
