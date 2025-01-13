import random
import unittest

from evaluation.models import Question, PointOfViewSetAnswer, Participant, CommentSelection, Comment
from evaluation.models.AnswerRepository import CommentAnswer
from evaluationDashboard.services.StatisticsService import StatisticsService


class StatisticsServiceTests(unittest.TestCase):
    def setUp(self):
        self.create_questions_db_entries()
        self.create_comment_selection_db_entries()
        self.create_participant_entries_in_db()
        self.create_comment_entries_in_db()

    def create_comment_entries_in_db(self):
        self.comments = []

        comments_counter = 1
        for comment_selection in self.comment_selections:
            for i in range(3):
                self.comments.append(Comment.objects.create(comment_selection=comment_selection, text=f"I am comment {comments_counter}"))
                comments_counter += 1

    def create_participant_entries_in_db(self):
        self.participant_1 = Participant.objects.create_user(username="Alice", password="1234")
        self.participant_2 = Participant.objects.create_user(username="Bob", password="1234")
        self.participant_3 = Participant.objects.create_user(username="Charlie", password="1234")

    def create_comment_selection_db_entries(self):
        self.comment_selections = []

        for question in self.questions:
            for method in ["random", "emotion", "sentiment", "stance", "news-agency"]:
                self.comment_selections.append(CommentSelection.objects.create(question_id=question.id, recommendation_method=method))

    def create_questions_db_entries(self):
        self.questions = [Question.objects.create(user_comment="User comment 1", article_title="Article Title 1", article_keywords="[Keyword 1, Keyword 2, Keyword 3]", news_agency="news agency 1"),
                          Question.objects.create(user_comment="User comment 2", article_title="Article Title 2", article_keywords="[Keyword 1, Keyword 5, Keyword 6]", news_agency="news agency 2"),
                          Question.objects.create(user_comment="User comment 3", article_title="Article Title 3", article_keywords="[Keyword 7, Keyword 9, Keyword 9]", news_agency="news agency 1"), ]

    def tearDown(self):
        Question.objects.all().delete()
        Participant.objects.all().delete()
        PointOfViewSetAnswer.objects.all().delete()
        CommentSelection.objects.all().delete()
        Comment.objects.all().delete()
        CommentAnswer.objects.all().delete()

    def test_get_statistics_number_of_user_comments(self):
        number_of_questions = StatisticsService.get_number_of_questions()

        self.assertEqual(number_of_questions, 3)  # add assertion here

    def test_get_statistics_number_of_completed_studies_all_participants_finished(self):
        self.answer_all_point_of_view_questions_for_participant_1_and_2()

        number_of_completed_studies = StatisticsService.get_number_of_completed_studies()

        self.assertEqual(number_of_completed_studies, 2)

    def answer_all_point_of_view_questions_for_participant_1_and_2(self):
        for participant in [self.participant_1, self.participant_2]:
            for question in self.questions:
                for comment_selection in [comment_selection for comment_selection in self.comment_selections if comment_selection.question_id == question.id]:
                    PointOfViewSetAnswer.objects.create(participant=participant, question=question,
                                                        recommendation_method=comment_selection.recommendation_method,
                                                        selected_method=random.choice(["random", "emotion", "sentiment", "stance", "news-agency"]))

    def test_get_number_of_participants(self):
        number_of_participants = StatisticsService.get_number_of_participants()

        self.assertEqual(number_of_participants, 3)

    def test_compute_percentages_for_point_of_view_questions_no_questions_answered_yet(self):
        question_id, model_percentages = StatisticsService.compute_percentages_for_point_of_view_questions()

        self.assertEqual(model_percentages[0], 0)
        self.assertEqual(model_percentages[1], 0)
        self.assertEqual(model_percentages[2], 0)

    def test_compute_percentages_for_point_of_view_questions_all_questions_answered(self):
        answer_participant_1 = ["random", "stance", "stance"]
        answer_participant_2 = ["stance", "random", "stance"]
        answer_participant_3 = ["stance", "random", "stance"]
        i = 0

        for question in self.questions:
            PointOfViewSetAnswer.objects.create(participant=self.participant_1, question=question,
                                                recommendation_method="stance",
                                                selected_method=answer_participant_1[i])

            PointOfViewSetAnswer.objects.create(participant=self.participant_2, question=question,
                                                recommendation_method="stance",
                                                selected_method=answer_participant_2[i])

            PointOfViewSetAnswer.objects.create(participant=self.participant_3, question=question,
                                                recommendation_method="stance",
                                                selected_method=answer_participant_3[i])
            i += 1

        question_id, model_percentages = StatisticsService.compute_percentages_for_point_of_view_questions()

        self.assertAlmostEqual(model_percentages[0], 67, 2)
        self.assertAlmostEqual(model_percentages[1], 33, 2)
        self.assertAlmostEqual(model_percentages[2], 100, 2)

    def test_compute_percentages_for_point_of_view_questions_some_questions_answered(self):
        answer_participant_1 = ["random", "stance"]
        answer_participant_2 = ["stance", "random"]
        answer_participant_3 = ["stance", "random"]
        i = 0

        for question in [self.questions[0], self.questions[2]]:
            PointOfViewSetAnswer.objects.create(participant=self.participant_1, question=question,
                                                recommendation_method="stance",
                                                selected_method=answer_participant_1[i])

            PointOfViewSetAnswer.objects.create(participant=self.participant_2, question=question,
                                                recommendation_method="stance",
                                                selected_method=answer_participant_2[i])

            PointOfViewSetAnswer.objects.create(participant=self.participant_3, question=question,
                                                recommendation_method="stance",
                                                selected_method=answer_participant_3[i])
            i += 1

        question_id, model_percentages = StatisticsService.compute_percentages_for_point_of_view_questions()

        self.assertAlmostEqual(model_percentages[0], 67, 2)
        self.assertAlmostEqual(model_percentages[1], 0, 2)
        self.assertAlmostEqual(model_percentages[2], 33, 2)

    def test_compute_percentages_for_point_of_view_questions_all_questions_answered_and_participant_has_no_answered_yet(self):
        answer_participant_1 = ["random", "stance", "random"]
        answer_participant_2 = ["stance", "stance", "random"]
        i = 0

        for question in self.questions:
            PointOfViewSetAnswer.objects.create(participant=self.participant_1, question=question,
                                                recommendation_method="stance",
                                                selected_method=answer_participant_1[i])

            PointOfViewSetAnswer.objects.create(participant=self.participant_2, question=question,
                                                recommendation_method="stance",
                                                selected_method=answer_participant_2[i])

            i += 1

        question_id, model_percentages = StatisticsService.compute_percentages_for_point_of_view_questions()

        self.assertAlmostEqual(model_percentages[0], 50, 2)
        self.assertAlmostEqual(model_percentages[1], 100, 2)
        self.assertAlmostEqual(model_percentages[2], 0, 2)

    def test_compute_percentages_for_point_of_view_questions_all_questions_answered_check_question_ids(self):
        self.generate_point_of_view_answers()

        question_id, model_percentages = StatisticsService.compute_percentages_for_point_of_view_questions()

        self.assertListEqual(question_id, [question.id for question in self.questions])

    def generate_point_of_view_answers(self):
        answer_participant_1 = ["random", "stance", "stance"]
        answer_participant_2 = ["stance", "random", "stance"]
        answer_participant_3 = ["stance", "random", "stance"]
        i = 0
        for question in self.questions:
            PointOfViewSetAnswer.objects.create(participant=self.participant_1, question=question,
                                                recommendation_method="stance",
                                                selected_method=answer_participant_1[i])

            PointOfViewSetAnswer.objects.create(participant=self.participant_2, question=question,
                                                recommendation_method="stance",
                                                selected_method=answer_participant_2[i])

            PointOfViewSetAnswer.objects.create(participant=self.participant_3, question=question,
                                                recommendation_method="stance",
                                                selected_method=answer_participant_3[i])
            i += 1

    def test_compute_percentage_comment_questions_no_model_comment_questions_answered_yet(self):
        question_ids, percentages = StatisticsService.compute_percentages_comment_questions(["stance", "emotion", "sentiment", "news-agency"])

        self.assertEqual(percentages[0], 0)
        self.assertEqual(percentages[1], 0)
        self.assertEqual(percentages[2], 0)

    def test_compute_percentage_comment_questions_no_random_comment_questions_answered_yet(self):
        question_ids, percentages = StatisticsService.compute_percentages_comment_questions(["random"])

        self.assertEqual(percentages[0], 0)
        self.assertEqual(percentages[1], 0)
        self.assertEqual(percentages[2], 0)

    def test_compute_percentage_comment_questions_all_model_comment_questions_answered(self):
        self.generate_comment_questions_answers()

        question_ids, percentages = StatisticsService.compute_percentages_comment_questions(["stance", "emotion", "sentiment", "news-agency"])

        self.assertAlmostEqual(percentages[0], 44, 2)
        self.assertAlmostEqual(percentages[1], 11, 2)
        self.assertAlmostEqual(percentages[2], 78, 2)

    def generate_comment_questions_answers(self):
        answer_participant_1 = [True, True, True, False, True, False, True, True, True]
        answer_participant_2 = [False, True, False, False, False, False, True, True, False]
        answer_participant_3 = [False, False, False, False, False, False, True, True, False]
        i = 0
        for question in self.questions:
            for comment_selection in [selection for selection in self.comment_selections if selection.question == question
                                                                                            and selection.recommendation_method in ["stance", "random"]]:
                for comment in [c for c in self.comments if comment_selection == c.comment_selection]:
                    if comment_selection.recommendation_method == "stance":
                        CommentAnswer.objects.create(participant=self.participant_1, question=question, comment_selection=comment_selection, comment=comment,
                                                     good_recommendation=answer_participant_1[i])
                        i += 1
                    else:
                        CommentAnswer.objects.create(participant=self.participant_1, question=question, comment_selection=comment_selection, comment=comment,
                                                     good_recommendation=not answer_participant_1[i])
        i = 0
        for question in self.questions:
            for comment_selection in [selection for selection in self.comment_selections if selection.question == question
                                                                                            and selection.recommendation_method in ["emotion", "random"]]:
                for comment in [c for c in self.comments if comment_selection == c.comment_selection]:
                    if comment_selection.recommendation_method == "emotion":
                        CommentAnswer.objects.create(participant=self.participant_2, question=question, comment_selection=comment_selection, comment=comment,
                                                     good_recommendation=answer_participant_2[i])
                        i += 1
                    else:
                        CommentAnswer.objects.create(participant=self.participant_2, question=question, comment_selection=comment_selection, comment=comment,
                                                     good_recommendation=not answer_participant_2[i])
        i = 0
        for question in self.questions:
            for comment_selection in [selection for selection in self.comment_selections if selection.question == question
                                                                                            and selection.recommendation_method in ["news-agency", "random"]]:
                for comment in [c for c in self.comments if comment_selection == c.comment_selection]:
                    if comment_selection.recommendation_method == "news-agency":
                        CommentAnswer.objects.create(participant=self.participant_3, question=question, comment_selection=comment_selection, comment=comment,
                                                     good_recommendation=answer_participant_3[i])
                        i += 1
                    else:
                        CommentAnswer.objects.create(participant=self.participant_3, question=question, comment_selection=comment_selection, comment=comment,
                                                     good_recommendation=not answer_participant_3[i])

    def test_compute_percentage_comment_questions_all_random_comment_questions_answered(self):
        answer_participant_1 = [True, False, True, False, True, False, True, True, True]
        answer_participant_2 = [False, True, False, False, True, False, True, True, False]
        answer_participant_3 = [False, False, False, False, False, False, True, False, False]
        i = 0
        j = 0
        for question in self.questions:
            for comment_selection in [selection for selection in self.comment_selections if selection.question == question
                                                                                            and selection.recommendation_method in ["random", "emotion"]]:
                for comment in [c for c in self.comments if comment_selection == c.comment_selection]:
                    if comment_selection.recommendation_method == "random":
                        CommentAnswer.objects.create(participant=self.participant_1, question=question, comment_selection=comment_selection, comment=comment,
                                                     good_recommendation=answer_participant_1[i])
                        CommentAnswer.objects.create(participant=self.participant_2, question=question, comment_selection=comment_selection, comment=comment,
                                                     good_recommendation=answer_participant_2[i])
                        CommentAnswer.objects.create(participant=self.participant_3, question=question, comment_selection=comment_selection, comment=comment,
                                                     good_recommendation=answer_participant_3[i])
                        i += 1
                    else:
                        CommentAnswer.objects.create(participant=self.participant_1, question=question, comment_selection=comment_selection, comment=comment,
                                                     good_recommendation=not answer_participant_1[j])
                        CommentAnswer.objects.create(participant=self.participant_2, question=question, comment_selection=comment_selection, comment=comment,
                                                     good_recommendation=not answer_participant_2[j])
                        CommentAnswer.objects.create(participant=self.participant_3, question=question, comment_selection=comment_selection, comment=comment,
                                                     good_recommendation=not answer_participant_3[j])
                        j += 1

        question_ids, percentages = StatisticsService.compute_percentages_comment_questions(["random"])

    def test_compute_average_percentages_for_questions_no_questions_answered(self):

        _, percentages = StatisticsService.compute_percentages_comment_questions(["stance", "emotion", "sentiment", "news-agency"])
        average_percentage = StatisticsService.compute_average_percentages_for_questions(percentages)

        self.assertEqual(average_percentage, 0)

    def test_compute_average_percentage_for_questions_all_questions_answered_model_recommendation_method(self):
        self.generate_comment_questions_answers()

        _, percentages = StatisticsService.compute_percentages_comment_questions(["stance", "emotion", "sentiment", "news-agency"])
        average_percentage = StatisticsService.compute_average_percentages_for_questions(percentages)

        self.assertAlmostEqual(average_percentage, 44.33, 2)

    def test_get_standard_deviation_average_percentages_for_questions_no_question_answered(self):
        _, percentages = StatisticsService.compute_percentages_comment_questions(["stance", "emotion", "sentiment", "news-agency"])

        standard_deviation = StatisticsService.get_standard_deviation_average_percentages_for_questions(percentages)

        self.assertEqual(standard_deviation, 0)

    def test_get_standard_deviation_average_percentage_for_questions_all_questions_answered(self):
        self.generate_comment_questions_answers()

        _, percentages = StatisticsService.compute_percentages_comment_questions(["stance", "emotion", "sentiment", "news-agency"])
        standard_deviation = StatisticsService.get_standard_deviation_average_percentages_for_questions(percentages)

        self.assertAlmostEqual(standard_deviation, 33.50, 2)

    def test_compute_topic_comment_percentages_no_questions_answered(self):
        percentages = StatisticsService.compute_topic_comment_percentages(["Keyword 1", "Keyword 4", "Keyword 7"], ["stance", "sentiment", "emotion", "news-agency"])

        self.assertListEqual([0, 0, 0], percentages)

    def test_compute_topic_comment_percentages_all_questions_answered(self):
        self.generate_comment_questions_answers()

        percentages = StatisticsService.compute_topic_comment_percentages(["Keyword 1", "Keyword 7"],
                                                                          ["stance", "sentiment", "emotion", "news-agency"])

        self.assertAlmostEqual(percentages[0], 27.77, 2)
        self.assertAlmostEqual(percentages[1], 77.78, 2)

    def test_compute_topic_point_of_view_percentages_no_questions_answered(self):
        percentages = StatisticsService.compute_topic_point_of_view_percentages(["Keyword 1", "Keyword 7"])

        self.assertEqual(percentages[0], 0)
        self.assertEqual(percentages[0], 0)

    def test_compute_topic_point_of_view_percentages_all_questions_answered(self):
        self.generate_point_of_view_answers()

        percentages = StatisticsService.compute_topic_point_of_view_percentages(["Keyword 1", "Keyword 7"])

        self.assertAlmostEqual(percentages[0], 50, 2)
        self.assertAlmostEqual(percentages[1], 100, 2)

    def test_compute_news_agencies_comment_percentages_no_questions_answered(self):
        percentages = StatisticsService.compute_news_agencies_comment_percentages(["new agency 1", "new agency 2"],
                                                                                  ["stance", "sentiment", "emotion", "news-agency"])

        self.assertEqual(percentages[0], 0)
        self.assertEqual(percentages[1], 0)

    def test_compute_news_agencies_comment_percentages_all_questions_answered(self):
        self.generate_comment_questions_answers()

        percentages = StatisticsService.compute_news_agencies_comment_percentages(["news agency 1", "news agency 2"],
                                                                                  ["stance", "sentiment", "emotion", "news-agency"])

        self.assertAlmostEqual(percentages[0], 61.11, 2)
        self.assertAlmostEqual(percentages[1], 11.11, 2)

    def test_compute_news_agencies_point_of_view_percentages_no_questions_answere(self):
        percentages = StatisticsService.compute_news_agencies_point_of_view_percentages(["news agency 1", "news agency 2"])
        self.assertEqual(percentages[0], 0)
        self.assertEqual(percentages[1], 0)

    def test_compute_news_agencies_point_of_view_percentages_all_questions_answered(self):
        self.generate_point_of_view_answers()

        percentages = StatisticsService.compute_news_agencies_point_of_view_percentages(["news agency 1", "news agency 2"])

        self.assertAlmostEqual(percentages[0], 83.34, 2)
        self.assertAlmostEqual(percentages[1], 33.33, 2)

    def test_compute_model_vs_news_agency_percentages_comment_answers_no_questions_answered(self):
        percentages = StatisticsService.compute_model_vs_news_agency_percentages_comment_answers([["stance", "sentiment", "emotion"], ["news-agency"]])

        self.assertAlmostEqual(percentages[0], 0, 2)
        self.assertAlmostEqual(percentages[1], 0, 2)

    def test_compute_model_vs_news_agency_percentages_comment_answers(self):
        self.generate_comment_questions_answers()

        percentages = StatisticsService.compute_model_vs_news_agency_percentages_comment_answers([["stance", "sentiment", "emotion"], ["news-agency"]])

        self.assertAlmostEqual(percentages[0], 55.67, 2)
        self.assertAlmostEqual(percentages[1], 22.33, 2)

    def test_compute_model_vs_news_agency_percentages_point_of_view_questions(self):
        answer_participant_1 = ["random", "stance", "stance"]
        answer_participant_2 = ["stance", "random", "random"]
        answer_participant_3 = ["news-agency", "random", "news-agency"]
        i = 0
        for question in self.questions:
            PointOfViewSetAnswer.objects.create(participant=self.participant_1, question=question,
                                                recommendation_method="stance",
                                                selected_method=answer_participant_1[i])

            PointOfViewSetAnswer.objects.create(participant=self.participant_2, question=question,
                                                recommendation_method="stance",
                                                selected_method=answer_participant_2[i])

            PointOfViewSetAnswer.objects.create(participant=self.participant_3, question=question,
                                                recommendation_method="news-agency",
                                                selected_method=answer_participant_3[i])
            i += 1

        percentages = StatisticsService.compute_model_vs_news_agency_percentages_point_of_view_questions([["stance", "sentiment", "emotion"], ["news-agency"]])

        self.assertAlmostEqual(percentages[0], 50, 2)
        self.assertAlmostEqual(percentages[1], 66.67, 2)

    def test_compute_model_vs_news_agency_percentages_point_of_view_questions_no_questions_answered(self):
        percentages = StatisticsService.compute_model_vs_news_agency_percentages_point_of_view_questions([["stance", "sentiment", "emotion"], ["news-agency"]])

        self.assertEqual(percentages[0], 0)
        self.assertEqual(percentages[1], 0)

    def test_all_statistics_present_in_dict(self):
        statistics_keys = StatisticsService.get_statistics().keys()

        self.assertEqual(len(statistics_keys), 9)
        self.assertIn("NumberOfUserComments", statistics_keys)
        self.assertIn("NumberOfCompletedStudies", statistics_keys)
        self.assertIn("NumberOfParticipants", statistics_keys)
        self.assertIn("CommentQuestions", statistics_keys)
        self.assertIn("PointOfViewQuestions", statistics_keys)
        self.assertIn("AveragePercentagePerTopics", statistics_keys)
        self.assertIn("AveragePercentagePerNewsAgency", statistics_keys)
        self.assertIn("ModelVsNewsAgencyRecommendationPercentages", statistics_keys)

    if __name__ == '__main__':
        unittest.main()
