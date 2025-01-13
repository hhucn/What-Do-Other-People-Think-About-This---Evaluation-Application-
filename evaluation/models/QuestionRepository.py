import random
from typing import List

from evaluation.domain.DomainCommentQuestion import DomainCommentQuestion
from evaluation.domain.PointOfViewQuestion import PointOfViewQuestion as DomainQuestion, PointOfViewQuestion
from evaluation.models import Participant
from evaluation.models.CommentRepository import CommentSelectionRepository
from evaluation.models.Questions import Question as ModelQuestion, Question
from evaluation.models.utils.clean_text import remove_html_tags


class QuestionRepository:
    @staticmethod
    def get_point_of_view_questions() -> List[DomainQuestion]:
        db_questions = ModelQuestion.objects.all()

        questions = []
        for question in db_questions:
            model_methods = ["stance", "sentiment", "emotion", "news-agency"]
            for model_method in model_methods:
                model_comment_selection = CommentSelectionRepository.load_comment_selection(question, model_method)
                random_comment_selection = CommentSelectionRepository.load_comment_selection(question, "random")
                comment_selections = [model_comment_selection, random_comment_selection]
                random.shuffle(comment_selections)
                questions.append(DomainQuestion(question_id=question.id, user_comment=remove_html_tags(question.user_comment),
                                                article_keywords=question.article_keywords, article_title=question.article_title, comment_selections=comment_selections,
                                                news_agency=question.news_agency, recommendation_method=model_method))

        return questions

    # TODO: Prüfen, ob gelöscht werden kann
    @staticmethod
    def load_question(question_id, recommendation_method: str):
        model_question: ModelQuestion = ModelQuestion.objects.get(id=question_id)
        comment_selections = CommentSelectionRepository.load_comment_selection(model_question, recommendation_method)
        return DomainQuestion(question_id=model_question.id, user_comment=model_question.user_comment,
                              article_keywords=model_question.article_keywords, article_title=model_question.article_title, comment_selections=comment_selections,
                              news_agency=model_question.news_agency, recommendation_method=recommendation_method)

    @classmethod
    def get_comment_question(cls, participant_id: int, question_id: int, recommendation_method: str) -> DomainCommentQuestion:
        print("Get Comment Question")
        participant: Participant = Participant.objects.get(id=participant_id)
        comment_answers = [answer.comment.id for answer in participant.CommentAnswers.get_queryset()]
        question = ModelQuestion.objects.get(pk=question_id)
        recommendation_comment_selection = CommentSelectionRepository.load_comment_selection(question, recommendation_method)
        random_comment_selection = CommentSelectionRepository.load_comment_selection(question, "random")

        comments = [comment for comment in recommendation_comment_selection.get_comments() if comment.id not in comment_answers]
        [comments.append(comment) for comment in random_comment_selection.get_comments() if comment.id not in comment_answers]

        if len(comments) > 0:
            comment = random.choice(comments)
            return DomainCommentQuestion(question=question, comment_selection=None, comment=comment,
                                         recommendation_method=recommendation_method)

        return None

    @classmethod
    def get_next_question(cls, participant_id: int) -> DomainCommentQuestion:
        participant = Participant.objects.get(pk=participant_id)
        questions = Question.objects.all()
        questions = [question for question in questions]
        point_of_view_answers_question_ids = [answer.question.id for answer in participant.PointOfViewAnswers.get_queryset() if
                                              answer.recommendation_method != "news-agency"]
        point_of_view_answers_news_agency_question_ids = [answer.question.id for answer in participant.PointOfViewAnswers.get_queryset() if
                                                          answer.recommendation_method == "news-agency"]
        print(f"Answered point of view questions: {point_of_view_answers_question_ids}")

        random.shuffle(questions)

        comment_question = []
        for question in questions:
            if question.id not in point_of_view_answers_question_ids:
                model_method = random.choice(["stance", "sentiment", "emotion"])
                model_comment_selection = CommentSelectionRepository.load_comment_selection(question, model_method)
                random_comment_selection = CommentSelectionRepository.load_comment_selection(question, "random")
                comment_selection = random.choice([model_comment_selection, random_comment_selection])
                comment = random.choice(comment_selection.get_comments())
                comment_question.append(DomainCommentQuestion(question=question, comment_selection=comment_selection, comment=comment,
                                                              recommendation_method=model_method))
            if question.id not in point_of_view_answers_news_agency_question_ids:
                model_comment_selection = CommentSelectionRepository.load_comment_selection(question, "news-agency")
                random_comment_selection = CommentSelectionRepository.load_comment_selection(question, "random")
                comment_selection = random.choice([model_comment_selection, random_comment_selection])
                comment = random.choice(comment_selection.get_comments())
                comment_question.append(DomainCommentQuestion(question=question, comment_selection=comment_selection, comment=comment,
                                                              recommendation_method='news-agency'))

        return random.choice(comment_question) if len(comment_question) > 0 else None

    @classmethod
    def get_point_of_view_question(cls, question_id: int, recommendation_method: str) -> PointOfViewQuestion:
        print("Get point of view question")
        question = Question.objects.get(pk=question_id)
        recommendation_comment_selection = CommentSelectionRepository.load_comment_selection(question, recommendation_method)
        random_comment_selection = CommentSelectionRepository.load_comment_selection(question, "random")

        comment_selection = [recommendation_comment_selection, random_comment_selection]

        random.shuffle(comment_selection)

        return PointOfViewQuestion(question_id=question_id, user_comment=remove_html_tags(question.user_comment), news_agency=question.news_agency,
                                   article_keywords=question.article_keywords, article_title=question.article_title, comment_selections=comment_selection,
                                   recommendation_method=recommendation_method)

    @classmethod
    def get_last_accessed_question(cls, participant):
        question = Question.objects.get(pk=participant.last_accessed_question_id)

        next_question = cls.get_comment_question(participant_id=participant.id, question_id=question.id, recommendation_method=participant.last_accessed_question_recommendation_method)

        if next_question is None:
            next_question = cls.get_point_of_view_question(question_id=question.id, recommendation_method=participant.last_accessed_question_recommendation_method)

        return next_question
