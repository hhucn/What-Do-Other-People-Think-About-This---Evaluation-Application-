from random import shuffle

from evaluation.domain.Participant import Participant as DomainParticipant
from evaluation.models import PointOfViewSetAnswer, Question
from evaluation.models.CommentRepository import CommentSelectionRepository
from evaluation.models.Participant import Participant
from evaluation.models.QuestionRepository import QuestionRepository


class ParticipantRepository:

    @staticmethod
    def load_participant(participant_id: int) -> DomainParticipant:
        db_participant = Participant.objects.get(id=participant_id)

        answered_questions = [[a.question.id, a.recommendation_method] for a in PointOfViewSetAnswer.objects.filter(participant_id=db_participant.id)]

        questions = QuestionRepository.get_point_of_view_questions()

        processed_questions = []
        unprocessed_questions = []

        for question in questions:
            if [question.get_id(), question.get_model_method()] in answered_questions:
                processed_questions.append(question)
            else:
                unprocessed_questions.append(question)

        shuffle(unprocessed_questions)

        if len(unprocessed_questions) > 0:
            next_question = unprocessed_questions[0]
        else:
            next_question = None

        progress = round(len(processed_questions) / len(questions) * 100, ndigits=2)

        return DomainParticipant(participant_id=db_participant.id, user_name=db_participant.username, processed_questions=processed_questions,
                                 next_question=next_question, progress=progress)

    @staticmethod
    def load_participant_with_next_question(participant_id):
        participant: Participant = Participant.objects.get(id=participant_id)

        if participant.last_accessed_question_id != -1:
            print("Get last accessed question")
            next_question = QuestionRepository.get_last_accessed_question(participant)
        else:
            next_question = QuestionRepository.get_next_question(participant_id)
            if next_question is None:
                return DomainParticipant(participant_id=participant.id, user_name=participant.username, processed_questions=None, next_question=None,
                                         progress=100.0)

            participant.last_accessed_question_id = next_question.question.id
            participant.last_accessed_question_recommendation_method = next_question.recommendation_method
            participant.save()

        progress = ParticipantRepository.calculate_progress(participant)
        return DomainParticipant(participant_id=participant.id, user_name=participant.username, next_question=next_question, progress=progress,
                                 processed_questions=None)

    @staticmethod
    def load_participant_with_next_comment_question(participant_id: int, question_id: int, recommendation_method: str):
        participant: Participant = Participant.objects.get(id=participant_id)

        next_question = QuestionRepository.get_comment_question(participant_id, question_id, recommendation_method)

        progress = ParticipantRepository.calculate_progress(participant)

        return DomainParticipant(participant_id=participant.id, user_name=participant.username, next_question=next_question, progress=progress,
                                 processed_questions=None)

    @staticmethod
    def calculate_progress(participant):
        point_of_view_answers = participant.CommentAnswers.get_queryset()
        questions = Question.objects.all()
        comments = []
        for question in questions:
            recommendation_method = CommentSelectionRepository.load_comment_selection(question, "stance")
            comments.extend(recommendation_method.get_comments())
            recommendation_method = CommentSelectionRepository.load_comment_selection(question, "news-agency")
            comments.extend(recommendation_method.get_comments())
            random_recommendations = CommentSelectionRepository.load_comment_selection(question, "random")
            comments.extend(random_recommendations.get_comments())
        progress = round(len(point_of_view_answers) / (len(comments)) * 100, 2)
        return progress

    @staticmethod
    def load_participant_with_point_of_view_question(participant_id, question_id, recommendation_method):
        participant: Participant = Participant.objects.get(id=participant_id)

        next_question = QuestionRepository.get_point_of_view_question(question_id, recommendation_method)

        progress = ParticipantRepository.calculate_progress(participant)

        return DomainParticipant(participant_id=participant.id, user_name=participant.username, next_question=next_question, progress=progress,
                                 processed_questions=None)
