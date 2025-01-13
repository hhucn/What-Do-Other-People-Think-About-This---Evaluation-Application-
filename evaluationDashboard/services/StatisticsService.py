import statistics
from typing import List

from evaluation.models import Question, PointOfViewSetAnswer
from evaluation.models.AnswerRepository import CommentAnswer
from evaluation.models.Participant import Participant


class StatisticsService:

    @classmethod
    def get_statistics(cls):
        return {
            "NumberOfUserComments": cls.get_number_of_questions(),
            "NumberOfCompletedStudies": cls.get_number_of_completed_studies(),
            "NumberOfParticipants": cls.get_number_of_participants(),
            "PercentageOfCompletedStudies": round(cls.get_number_of_completed_studies() / cls.get_number_of_participants() * 100, ndigits=2),
            "CommentQuestions": cls.get_percentages_for_all_comment_questions(),
            "PointOfViewQuestions": cls.get_percentages_for_all_point_of_view_questions(),
            "AveragePercentagePerTopics": cls.get_average_percentage_for_topics(),
            "AveragePercentagePerNewsAgency": cls.get_average_percentage_for_news_agencies(),
            "ModelVsNewsAgencyRecommendationPercentages": cls.get_percentages_model_vs_news_agency()
        }

    @staticmethod
    def get_number_of_completed_studies():
        participants = Participant.objects.all()
        questions = Question.objects.all()

        count = 0

        for participant in participants:
            answers = PointOfViewSetAnswer.objects.filter(participant_id=participant.id)
            if len(answers) >= len(questions):
                count += 1

        return count

    @staticmethod
    def get_number_of_questions():
        questions = Question.objects.all()
        return len(questions)

    @staticmethod
    def get_number_of_participants():
        participants = Participant.objects.all()
        return len(participants)

    @staticmethod
    def compute_percentages_for_point_of_view_questions():
        questions = Question.objects.all()
        percentages = []
        question_ids = []

        for question in questions:
            answers = PointOfViewSetAnswer.objects.filter(question=question)
            good_recommendation_answers = [answer for answer in answers if answer.selected_method == answer.recommendation_method]
            if len(answers) > 0:
                percentages.append(round(len(good_recommendation_answers) / float(len(answers)), 2) * 100)
            else:
                percentages.append(0)
            question_ids.append(question.id)
        return question_ids, percentages

    @staticmethod
    def compute_percentages_comment_questions(recommendation_methods: List[str]):
        questions = Question.objects.all()
        percentages = []
        question_ids = []

        for question in questions:
            answers = CommentAnswer.objects.filter(question=question)
            model_answers = [answer for answer in answers if answer.comment_selection.recommendation_method in recommendation_methods]
            good_recommendation_answers = [answer for answer in model_answers if answer.good_recommendation]
            if len(model_answers) > 0:
                percentages.append(round(len(good_recommendation_answers) / float(len(model_answers)), 2) * 100)
            else:
                percentages.append(0)
            question_ids.append(question.id)

        return question_ids, percentages

    @staticmethod
    def compute_average_percentages_for_questions(percentages):
        return round(sum(percentages) / len(percentages), 2) if len(percentages) > 0 else 0

    @staticmethod
    def get_standard_deviation_average_percentages_for_questions(percentages):
        return round(statistics.stdev(percentages), 2) if len(percentages) > 1 else 0

    @classmethod
    def get_percentages_for_all_comment_questions(cls):
        question_ids, model_percentages = cls.compute_percentages_comment_questions(["stance", "sentiment", "emotion", "news-agency"])
        question_ids, random_percentages = cls.compute_percentages_comment_questions(["random"])

        return {
            "average_percentage_model": cls.compute_average_percentages_for_questions(model_percentages),
            "standard_deviation_model": cls.get_standard_deviation_average_percentages_for_questions(model_percentages),
            "average_percentage_random": cls.compute_average_percentages_for_questions(random_percentages),
            "standard_deviation_random": cls.get_standard_deviation_average_percentages_for_questions(random_percentages),
            "PercentagesForCommentQuestions": {
                "question_ids": question_ids,
                "random_percentages": random_percentages,
                "model_percentages": model_percentages,
            }
        }

    @classmethod
    def get_percentages_for_all_point_of_view_questions(cls):
        question_ids, model_percentages = cls.compute_percentages_for_point_of_view_questions()

        return {
            "average_percentage_model": cls.compute_average_percentages_for_questions(model_percentages),
            "standard_deviation_model": cls.get_standard_deviation_average_percentages_for_questions(model_percentages),
            "PercentagesForPointOfViewQuestions": {
                "question_ids": question_ids,
                "model_percentages": model_percentages,
            }
        }

    @classmethod
    def get_average_percentage_for_topics(cls):
        topics = ["abortion", "trump", "global warming"]
        topics_comment_percentages_model = cls.compute_topic_comment_percentages(topics, ["stance", "sentiment", "emotion", "news-agency"])
        topics_comment_percentages_random = cls.compute_topic_comment_percentages(topics, ["random"])
        topics_point_of_view_percentages = cls.compute_topic_point_of_view_percentages(topics)

        return {
            "topics": topics,
            "CommentAnswer": {
                "model": topics_comment_percentages_model,
                "random": topics_comment_percentages_random
            },
            "PointOfViewAnswers": topics_point_of_view_percentages
        }

    @classmethod
    def compute_topic_comment_percentages(cls, topics, recommendation_method):
        questions = Question.objects.all()
        comment_percentages = []

        for topic in topics:
            topic_questions = [question for question in questions if topic.lower() in question.article_keywords.lower()]
            percentages = []
            for topic_question in topic_questions:
                comment_answers = [comment_answer for comment_answer in CommentAnswer.objects.filter(question=topic_question)
                                   if comment_answer.comment_selection.recommendation_method in recommendation_method]
                good_recommendations = [answer for answer in comment_answers if answer.good_recommendation]
                if len(comment_answers) > 0:
                    percentages.append(round(len(good_recommendations) / len(comment_answers) * 100, 2))
                else:
                    percentages.append(0)
            comment_percentages.append(cls.compute_average_percentages_for_questions(percentages))

        return comment_percentages

    @classmethod
    def compute_topic_point_of_view_percentages(cls, topics):
        questions = Question.objects.all()
        point_of_view_percentages = []

        for topic in topics:
            topic_questions = [question for question in questions if topic.lower() in question.article_keywords.lower()]
            percentages = []
            for topic_question in topic_questions:
                point_of_view_answers = PointOfViewSetAnswer.objects.filter(question=topic_question)
                good_recommendations = [answer for answer in point_of_view_answers if answer.recommendation_method == answer.selected_method]
                if len(point_of_view_answers) > 0:
                    percentages.append(round(len(good_recommendations) / len(point_of_view_answers) * 100, 2))
                else:
                    percentages.append(0)
            point_of_view_percentages.append(cls.compute_average_percentages_for_questions(percentages))

        return point_of_view_percentages

    @classmethod
    def get_average_percentage_for_news_agencies(cls):
        news_agencies = ["Breitbart", "NyTimes"]
        news_agencies_model_comment_percentages = cls.compute_news_agencies_comment_percentages(news_agencies,
                                                                                                ["stance", "sentiment", "emotion", "news-agency"])
        news_agencies_random_comment_percentages = cls.compute_news_agencies_comment_percentages(news_agencies,
                                                                                                 ["random"])
        news_agencies_point_of_view_percentages = cls.compute_news_agencies_point_of_view_percentages(news_agencies)

        return {
            "news_agencies": news_agencies,
            "CommentAnswer": {
                "model": news_agencies_model_comment_percentages,
                "random": news_agencies_random_comment_percentages
            },
            "PointOfViewAnswers": news_agencies_point_of_view_percentages
        }

    @classmethod
    def compute_news_agencies_comment_percentages(cls, news_agencies, recommendation_method):
        questions = Question.objects.all()
        comment_percentages = []

        for news_agency in news_agencies:
            news_agency_questions = [question for question in questions if news_agency == question.news_agency]
            percentages = []
            for news_agency_question in news_agency_questions:
                comment_answers = [answer for answer in CommentAnswer.objects.filter(question=news_agency_question)
                                   if answer.comment_selection.recommendation_method in recommendation_method]
                good_recommendations = [answer for answer in comment_answers if answer.good_recommendation]
                if len(comment_answers) > 0:
                    percentages.append(round(len(good_recommendations) / len(comment_answers) * 100, 2))
                else:
                    percentages.append(0)
            comment_percentages.append(cls.compute_average_percentages_for_questions(percentages))

        return comment_percentages

    @classmethod
    def compute_news_agencies_point_of_view_percentages(cls, news_agencies):
        questions = Question.objects.all()
        point_of_view_percentages = []

        for news_agency in news_agencies:
            news_agency_questions = [question for question in questions if news_agency == question.news_agency]
            percentages = []
            for news_agency_question in news_agency_questions:
                point_of_view_answers = PointOfViewSetAnswer.objects.filter(question=news_agency_question)
                good_recommendations = [answer for answer in point_of_view_answers if answer.recommendation_method == answer.selected_method]
                if len(point_of_view_answers) > 0:
                    percentages.append(round(len(good_recommendations) / len(point_of_view_answers) * 100, 2))
                else:
                    percentages.append(0)
            point_of_view_percentages.append(cls.compute_average_percentages_for_questions(percentages))

        return point_of_view_percentages

    @classmethod
    def compute_model_vs_news_agency_percentages_comment_answers(cls, methods):
        questions = Question.objects.all()
        average_percentages = []

        for method in methods:
            percentages = []
            for question in questions:
                answers = [answer for answer in CommentAnswer.objects.filter(question=question) if answer.comment_selection.recommendation_method in method]
                good_recommendation_answers = [answer for answer in answers if answer.good_recommendation]
                if len(answers) > 0:
                    percentages.append(round(len(good_recommendation_answers) / float(len(answers)), 2) * 100)
                else:
                    percentages.append(0)
            average_percentages.append(cls.compute_average_percentages_for_questions(percentages))

        return average_percentages

    @classmethod
    def get_percentages_model_vs_news_agency(cls):
        methods = [["stance", "sentiment", "emotion"], ["news-agency"]]

        return {
            "methods": methods,
            "CommentQuestions": cls.compute_model_vs_news_agency_percentages_comment_answers(methods),
            "PointOfViewQuestions": cls.compute_model_vs_news_agency_percentages_point_of_view_questions(methods)
        }

    @classmethod
    def compute_model_vs_news_agency_percentages_point_of_view_questions(cls, methods):
        questions = Question.objects.all()
        average_percentages = []

        for method in methods:
            percentages = []
            for question in questions:
                answers = [answer for answer in PointOfViewSetAnswer.objects.filter(question=question) if answer.recommendation_method in method]
                good_recommendation_answers = [answer for answer in answers if answer.recommendation_method == answer.selected_method]
                if len(answers) > 0:
                    percentages.append(round(len(good_recommendation_answers) / float(len(answers)), 2) * 100)
                else:
                    percentages.append(0)
            average_percentages.append(cls.compute_average_percentages_for_questions(percentages))

        return average_percentages
