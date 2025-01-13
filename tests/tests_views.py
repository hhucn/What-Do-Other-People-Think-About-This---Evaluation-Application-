from unittest import skip
from unittest.mock import Mock, patch

from django.contrib.sessions.middleware import SessionMiddleware
from django.db import IntegrityError
from django.test import Client
from django.test import TestCase, RequestFactory
from django.urls import reverse

from evaluation.applicationservice.EvaluationService import EvaluationService
from evaluation.domain.DomainCommentQuestion import DomainCommentQuestion
from evaluation.domain.Participant import Participant
from evaluation.models import CommentSelection, Comment
from evaluation.models.AnswerRepository import CommentAnswer
from evaluation.models.Participant import Participant as ModelParticipant
from evaluation.models.Questions import Question as ModelQuestion
from evaluation.views import QuestionView, PointOfViewAnswerView, CommentQuestionView


def capture_log_messages(message):
    capture_log_messages.messages.append(message)


# Initialize a list to hold captured log messages
capture_log_messages.messages = []


class ViewsTest(TestCase):

    def setUp(self):
        self.question_1 = ModelQuestion.objects.create(article_title="Article Title 1", article_keywords="Article Keywords 1", user_comment="User comment 1")
        self.question_2 = ModelQuestion.objects.create(article_title="Article Title 2", article_keywords="Article Keywords 2", user_comment="User comment 2")
        self.question_3 = ModelQuestion.objects.create(article_title="Article Title 3", article_keywords="Article Keywords 3", user_comment="User comment 3")

        self.comment_selection_1 = CommentSelection.objects.create(recommendation_method="news-agency", question_id=self.question_1.id)
        self.comment_selection_2 = CommentSelection.objects.create(recommendation_method="news-agency", question_id=self.question_2.id)
        self.comment_selection_3 = CommentSelection.objects.create(recommendation_method="news-agency", question_id=self.question_3.id)

        self.comment_selection_4 = CommentSelection.objects.create(recommendation_method="stance", question_id=self.question_1.id)
        self.comment_selection_5 = CommentSelection.objects.create(recommendation_method="stance", question_id=self.question_2.id)
        self.comment_selection_6 = CommentSelection.objects.create(recommendation_method="stance", question_id=self.question_3.id)

        self.comment_selection_7 = CommentSelection.objects.create(recommendation_method="sentiment", question_id=self.question_1.id)
        self.comment_selection_8 = CommentSelection.objects.create(recommendation_method="sentiment", question_id=self.question_2.id)
        self.comment_selection_9 = CommentSelection.objects.create(recommendation_method="sentiment", question_id=self.question_3.id)

        self.comment_selection_10 = CommentSelection.objects.create(recommendation_method="emotion", question_id=self.question_1.id)
        self.comment_selection_11 = CommentSelection.objects.create(recommendation_method="emotion", question_id=self.question_2.id)
        self.comment_selection_12 = CommentSelection.objects.create(recommendation_method="emotion", question_id=self.question_3.id)

        self.comment_selection_13 = CommentSelection.objects.create(recommendation_method="random", question_id=self.question_1.id)
        self.comment_selection_14 = CommentSelection.objects.create(recommendation_method="random", question_id=self.question_2.id)
        self.comment_selection_15 = CommentSelection.objects.create(recommendation_method="random", question_id=self.question_3.id)

        self.comment_1 = Comment.objects.create(comment_selection=self.comment_selection_1, text="I am a test comment")

        self.comment_question = DomainCommentQuestion(question=self.question_1, comment_selection=self.comment_selection_1, comment=self.comment_1, recommendation_method="stance")

    def tearDown(self):
        ModelQuestion.objects.all().delete()
        CommentSelection.objects.all().delete()
        Comment.objects.all().delete()
        ModelParticipant.objects.all().delete()

    def test_if_user_not_logged_in_redirect_to_login(self):
        client = Client()

        response = client.get(reverse("index"))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

    @patch('evaluation.applicationservice.EvaluationService.EvaluationService.get_participant_with_next_question')
    def test_if_user_logged_in_redirect_to_questions_page(self, get_next_question_mock):
        client = Client()
        participant = ModelParticipant.objects.create_user(username='Alice', password='iamgroot')
        client.force_login(participant)
        domain_participant = Participant(participant_id=participant.id, user_name="Alice", progress=0.0, processed_questions=[],
                                         next_question=DomainCommentQuestion(question=self.question_1, comment_selection=self.comment_selection_1, comment=self.comment_1, recommendation_method="stance"))

        get_next_question_mock.return_value = domain_participant

        response = client.get(reverse("index"))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("question"))

    @patch('evaluation.applicationservice.EvaluationService.EvaluationService.get_participant_with_next_question')
    def test_get_login_page(self, get_next_question_mock):
        client = Client()
        participant = ModelParticipant.objects.create_user(username="Groot", password="iamgroot")
        domain_participant = Participant(participant_id=participant.id, user_name="Groot", progress=0.0, processed_questions=[],
                                         next_question=DomainCommentQuestion(question=self.question_1, comment_selection=self.comment_selection_1, comment=self.comment_1, recommendation_method="stance"))

        get_next_question_mock.return_value = domain_participant

        response = client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    @patch('evaluation.applicationservice.EvaluationService.EvaluationService.get_participant_with_next_question')
    def test_login_a_user_that_is_not_authenticated_but_exists(self, get_next_question_mock):
        username = "Groot"
        password = "iamgroot"
        participant = ModelParticipant.objects.create_user(username=username, password=password)
        client = Client()
        domain_participant = Participant(participant_id=participant.id, user_name="Groot", progress=0.0, processed_questions=[],
                                         next_question=DomainCommentQuestion(question=self.question_1, comment_selection=self.comment_selection_1, comment=self.comment_1, recommendation_method="stance"))

        get_next_question_mock.return_value = domain_participant

        response = client.post(reverse("login"), {"username": username, "password": password})

        # Redirect to a protected view to see if login is successful
        self.assertRedirects(response, reverse("question"), status_code=302, target_status_code=200)

    def test_login_a_user_that_does_not_exist(self):
        client = Client()

        response = client.post(reverse("login"), {"username": "Groot", "password": "iamgroot"})

        self.assertRedirects(response, reverse("login"))

    def test_log_out_user(self):
        client = Client()
        participant = ModelParticipant.objects.create_user(username="Groot", password="iamgroot")
        client.force_login(participant)

        response = client.get(reverse("logout"))

        request = response.wsgi_request
        self.assertIsNotNone(request.session)
        # After logout response does not have session data
        with self.assertRaises(AttributeError):
            response.session

    @patch('evaluation.applicationservice.EvaluationService.EvaluationService.get_participant_with_next_question')
    def test_question_view_cannot_be_accessed_without_logged_in(self, get_next_question_mock):
        client = Client()
        participant = ModelParticipant.objects.create_user(username="Groot", password="iamgroot")
        domain_participant = Participant(participant_id=participant.id, user_name="Groot", progress=0.0, processed_questions=[],
                                         next_question=DomainCommentQuestion(question=self.question_1, comment_selection=self.comment_selection_1, comment=self.comment_1, recommendation_method="stance"))

        get_next_question_mock.return_value = domain_participant

        response = client.get(reverse("question"))

        self.assertEqual(response.status_code, 302)

        client.force_login(participant)
        response = client.get(reverse("question"))

        self.assertTemplateUsed(response, template_name="evaluation/comment_question.html")

    def test_questions_view_user_has_not_answered_questions_and_expect_first_question(self):
        question = DomainCommentQuestion(question=self.question_1, comment_selection=self.comment_selection_1, comment=self.comment_1,
                                         recommendation_method="stance")
        participant = Participant(participant_id=1, user_name="Groot", processed_questions=[], next_question=question, progress=0)
        model_participant = ModelParticipant.objects.create_user(username="Groot", password="iamgroot")
        evaluation_service_mock = Mock(EvaluationService)
        evaluation_service_mock.get_participant_with_next_question.return_value = participant
        request = self.produce_request_for_logged_in_user(model_participant)

        question_view = QuestionView(evaluation_service=evaluation_service_mock)
        question_view.setup(request)

        response = question_view.get(request)

        response.render()

        question_view.evaluation_service.get_participant_with_next_question.assert_called_with(model_participant.id, None, None)
        self.assertEqual(response.context_data["next_question"], question)
        self.assertEqual(response.template_name[0], "evaluation/comment_question.html")

    @patch('logging.Logger.error')
    def test_handle_integrity_error_by_duplicate_answer(self, mock_logger):
        mock_logger.side_effect = capture_log_messages
        evaluation_service_mock = Mock(EvaluationService)
        answer_view = PointOfViewAnswerView(evaluation_service=evaluation_service_mock)
        evaluation_service_mock.save_point_of_view_answer.side_effect = IntegrityError()
        request_factory = RequestFactory()
        middleware = SessionMiddleware(lambda x: None)
        request = request_factory.get(reverse("question"))
        middleware.process_request(request)
        request.session['_auth_user_id'] = 1
        request.session.save()

        answer_view.setup(request)

        response = answer_view.get(request, [], question_id=1, selection_id=1)

        self.assertIn('Cannot store duplicate answers', capture_log_messages.messages)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("question"))

    def produce_request_for_logged_in_user(self, user):
        request_factory = RequestFactory()
        middleware = SessionMiddleware(lambda x: None)
        request = request_factory.get(reverse("question"))
        request.user = user
        middleware.process_request(request)
        request.session['_auth_user_id'] = user.id
        request.session.save()
        return request

    def test_save_comment_answer_cannot_be_accessed_by_not_logged_in_user(self):
        client = Client()
        participant = ModelParticipant.objects.create_user(username="Groot", password="IamGroot")

        response = client.get(reverse("comment-answer", args=(1, 1, 1, True)))

        self.assertEqual(response.status_code, 302)

    @skip
    @patch('evaluation.applicationservice.EvaluationService.EvaluationService.get_participant_with_next_question')
    def test_save_comment_answer_logged_in_user_can_access(self, get_next_question_mock):
        client = Client()
        participant = ModelParticipant.objects.create_user(username="Groot", password="IamGroot")
        client.force_login(participant)

        response = client.get(reverse("comment-answer", args=(self.question_1.id, self.comment_selection_1.id, self.comment_1.id, True)))

        self.assertRedirects(response, reverse("question"))

    @skip
    def test_comment_answer_has_been_saved(self):
        client = Client()
        participant = ModelParticipant.objects.create_user(username="Groot", password="IamGroot")
        client.force_login(participant)

        response = client.get(reverse("comment-answer", args=(self.question_1.id, self.comment_selection_1.id, self.comment_1.id, True)))

        answers = CommentAnswer.objects.all()
        self.assertEqual(len(answers), 1)
        self.assertEqual(answers[0].question, self.question_1)

    def test_question_view_call_next_comment_question(self):
        question = DomainCommentQuestion(question=self.question_1, comment_selection=self.comment_selection_1, comment=self.comment_1, recommendation_method="stance")
        participant = Participant(participant_id=1, user_name="Groot", processed_questions=[], next_question=question, progress=0)
        model_participant = ModelParticipant.objects.create_user(username="Groot", password="iamgroot")
        evaluation_service_mock = Mock(EvaluationService)
        evaluation_service_mock.get_participant_with_next_question.return_value = participant

        request_factory = RequestFactory()
        middleware = SessionMiddleware(lambda x: None)
        request = request_factory.get(reverse("comment-question", args=(1, "stance")))
        request.user = model_participant
        middleware.process_request(request)
        request.session['_auth_user_id'] = model_participant.id
        request.session.save()
        view = CommentQuestionView(evaluation_service=evaluation_service_mock)
        view.setup(request)

        response = view.get(request)

        # TODO
        # view.evaluation_service.get_participant_with_next_question.assert_called_with(model_participant.id, self.question_1.id, "stance")
        self.assertEqual(response.context_data["next_question"], question)
        self.assertEqual(response.template_name[0], "evaluation/comment_question.html")
