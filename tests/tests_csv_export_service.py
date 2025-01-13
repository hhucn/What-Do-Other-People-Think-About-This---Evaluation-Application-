import unittest

from evaluation.models import Participant, Question, CommentSelection, PointOfViewSetAnswer, Comment
from evaluation.models.AnswerRepository import CommentAnswer
from evaluationDashboard.services.DemographicsService import DemographicsService
from evaluationDashboard.services.EvaluationDataService import EvaluationDataService


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.participant_1 = Participant.objects.create_user(username="Tony", password="IamIronMan", age=52, education="Master", gender="male")
        self.participant_2 = Participant.objects.create_user(username="Peter", password="IamSpiderMan", age=21, education="Bachelor", gender="male")
        self.participant_3 = Participant.objects.create_user(username="Groot", password="IamGroot", age=18, education="PHD", gender="None")
        self.participant_4 = Participant.objects.create_user(username="Natasha", password="IamBlackWidow", age=40, education="Highschool", gender="female")
        self.participant_5 = Participant.objects.create_user(username="Carol", password="IamCaptainMarvel", age=59, education="Master", gender="female")

        self.question_1 = Question.objects.create(user_comment="I am user comment 1")
        self.question_2 = Question.objects.create(user_comment="I am user comment 2")

        self.selection_1 = CommentSelection.objects.create(question=self.question_1, recommendation_method="Stance")
        self.selection_2 = CommentSelection.objects.create(question=self.question_1, recommendation_method="Sentiment")
        self.selection_3 = CommentSelection.objects.create(question=self.question_1, recommendation_method="Emotion")
        self.selection_4 = CommentSelection.objects.create(question=self.question_1, recommendation_method="NewsAgency")
        self.selection_5 = CommentSelection.objects.create(question=self.question_1, recommendation_method="Random")

        self.selection_6 = CommentSelection.objects.create(question=self.question_2, recommendation_method="Stance")
        self.selection_7 = CommentSelection.objects.create(question=self.question_2, recommendation_method="Sentiment")
        self.selection_8 = CommentSelection.objects.create(question=self.question_2, recommendation_method="Emotion")
        self.selection_9 = CommentSelection.objects.create(question=self.question_2, recommendation_method="NewsAgency")
        self.selection_10 = CommentSelection.objects.create(question=self.question_2, recommendation_method="Random")

        self.comment_1 = Comment.objects.create(comment_selection=self.selection_1, text="I am comment 1")
        self.comment_2 = Comment.objects.create(comment_selection=self.selection_1, text="I am comment 2")
        self.comment_3 = Comment.objects.create(comment_selection=self.selection_2, text="I am comment 3")
        self.comment_4 = Comment.objects.create(comment_selection=self.selection_2, text="I am comment 4")

        self.comment_answer_1 = CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.selection_1, comment=self.comment_1, good_recommendation=True)
        self.comment_answer_2 = CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.selection_1, comment=self.comment_2, good_recommendation=False)
        self.comment_answer_3 = CommentAnswer.objects.create(participant=self.participant_1, question=self.question_1, comment_selection=self.selection_2, comment=self.comment_3, good_recommendation=True)

        self.point_of_view_answer_1 = PointOfViewSetAnswer.objects.create(question=self.question_1, participant=self.participant_1, recommendation_method="Stance")
        self.point_of_view_answer_2 = PointOfViewSetAnswer.objects.create(question=self.question_1, participant=self.participant_1, recommendation_method="Random")
        self.point_of_view_answer_3 = PointOfViewSetAnswer.objects.create(question=self.question_2, participant=self.participant_2, recommendation_method="Sentiment")

    def tearDown(self):
        Participant.objects.all().delete()
        CommentSelection.objects.all().delete()
        PointOfViewSetAnswer.objects.all().delete()
        Question.objects.all().delete()
        Comment.objects.all().delete()
        CommentAnswer.objects.all().delete()

    def test_create_demographics_data(self):
        demographics = DemographicsService.get_demographics_data()

        self.assertEqual(len(demographics), 5)
        self.assertDictEqual({"username": "Tony", "age": 52, "education": "Master", "gender": "male"}, demographics[0])
        self.assertDictEqual({"username": "Peter", "age": 21, "education": "Bachelor", "gender": "male"}, demographics[1])
        self.assertDictEqual({"username": "Groot", "age": 18, "education": "PHD", "gender": "None"}, demographics[2])
        self.assertDictEqual({"username": "Natasha", "age": 40, "education": "Highschool", "gender": "female"}, demographics[3])
        self.assertDictEqual({"username": "Carol", "age": 59, "education": "Master", "gender": "female"}, demographics[4])

    def test_get_question_data(self):
        question_data = EvaluationDataService.get_question_data()

        self.assertEqual(len(question_data), 2)
        self.assertDictEqual({"question_id": self.question_1.id, "user_comment": self.question_1.user_comment, "article_title": self.question_1.article_title,
                              "keywords": self.question_1.article_keywords, "news_agency": self.question_1.news_agency}, question_data[0])
        self.assertDictEqual({"question_id": self.question_2.id, "user_comment": self.question_2.user_comment, "article_title": self.question_2.article_title,
                              "keywords": self.question_2.article_keywords, "news_agency": self.question_2.news_agency}, question_data[1])

    def test_get_comment_selection_data(self):
        comment_selection_data = EvaluationDataService.get_comment_selections()

        self.assertEqual(len(comment_selection_data), 10)

        self.assertDictEqual({
            "question_id": self.question_1.id,
            "recommendation_method": self.selection_1.recommendation_method,
        }, comment_selection_data[0])

    def test_get_comment_data(self):
        comment_data = EvaluationDataService.get_comments()

        self.assertEqual(len(comment_data), 4)
        self.assertDictEqual({"comment_selection": self.selection_1.id, "comment_id": self.comment_1.id, "text": "I am comment 1"}, comment_data[0])
        self.assertDictEqual({"comment_selection": self.selection_2.id, "comment_id": self.comment_3.id, "text": "I am comment 3"}, comment_data[2])

    def test_get_comment_answers(self):
        comment_answers_data = EvaluationDataService.get_comment_answers()

        self.assertEqual(len(comment_answers_data), 3)
        self.assertDictEqual(
            {"answer_id": self.comment_answer_1.id, "participant_id": self.comment_answer_1.participant_id, "question_id": self.comment_answer_1.question.id,
             "news_agency": self.comment_answer_1.question.news_agency,
             "keywords": self.comment_answer_1.question.article_keywords,
             "comment_selection_id": self.comment_answer_1.comment_selection.id,
             "comment_text": self.comment_answer_1.comment.text,
             "recommendation_method": self.comment_answer_1.comment_selection.recommendation_method, "comment_id": self.comment_answer_1.comment.id,
             "good_recommendation": self.comment_answer_1.good_recommendation},
            comment_answers_data[0])

    def test_get_point_of_view_answers(self):
        point_of_view_data = EvaluationDataService.get_point_of_view_answer_data()

        self.assertEqual(len(point_of_view_data), 3)
        self.assertDictEqual({
            "question_id": self.point_of_view_answer_1.question_id,
            "user_comment": self.point_of_view_answer_1.question.user_comment,
            "recommendation_method": self.point_of_view_answer_1.recommendation_method,
            "selected_recommendation_method": self.point_of_view_answer_1.selected_method,
            "keywords": self.point_of_view_answer_1.question.article_keywords,
            "news_agency": self.point_of_view_answer_1.question.news_agency,
            "participant_id": self.point_of_view_answer_1.participant_id
        }, point_of_view_data[0])

    def test_get_participant_data(self):
        participant_data = EvaluationDataService.get_participant_data()

        self.assertEqual(len(participant_data), 5)
        self.assertDictEqual({
            "participant_id": self.participant_1.id,
            "gender": self.participant_1.gender,
            "age": self.participant_1.age,
            "education": self.participant_1.education
        }, participant_data[0])


if __name__ == '__main__':
    unittest.main()
