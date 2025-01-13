import unittest
from unittest import skip
from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import reverse

from evaluation.models import Participant


def get_response_for_superuser():
    client = Client()
    participant = Participant.objects.create_user("Bob", password="1234", is_superuser=True)
    client.force_login(participant)
    response = client.get(reverse("dashboard_index"))
    return response


class ViewsDashboardTests(TestCase):

    def tearDown(self):
        Participant.objects.all().delete()

    def test_dashboard_view_with_not_logged_in_user_raise_403_forbidden(self):
        client = Client()
        response = client.get(reverse("dashboard_index"))

        self.assertEqual(response.status_code, 403)

    def test_dashboard_view_with_non_superuser_raise_403_forbidden(self):
        client = Client()
        participant = Participant.objects.create_user(username="Alice", password="iamgroot")
        client.force_login(participant)

        response = client.get(reverse("dashboard_index"))

        self.assertEqual(response.status_code, 403)

    @patch('evaluationDashboard.services.StatisticsService.StatisticsService.get_statistics')
    def test_dashboard_view_renders_dashboard_template(self, mock_statistics_service):
        mock_statistics_service.return_value = {}
        response = get_response_for_superuser()

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/statistics.html")

    @patch("evaluationDashboard.services.DemographicsService.DemographicsService.get_demographics")
    @patch('evaluationDashboard.services.StatisticsService.StatisticsService.get_statistics')
    def test_dashboard_view_response_contains_demographics(self, mock_demographics_service, mock_statistics_service):
        mock_statistics_service.return_value = {}
        mock_demographics_service.return_value = {}
        response = get_response_for_superuser()

        mock_demographics_service.assert_called_once()
        self.assertIn("demographics", response.context)

    @patch('evaluationDashboard.services.StatisticsService.StatisticsService.get_statistics')
    def test_dashboard_view_context_contains_statistics(self, mock_statistics_service):
        mock_statistics_service.return_value = {}

        response = get_response_for_superuser()

        mock_statistics_service.assert_called_once()
        self.assertIn("statistics", response.context)

    @patch("evaluationDashboard.services.DemographicsService.DemographicsService.get_demographics")
    @patch('evaluationDashboard.services.StatisticsService.StatisticsService.get_statistics')
    @skip("TODO: Fix test")
    def test_demographics_view_renders_demographics_template(self, demographics_service, mock_statistics_service):
        client = Client()
        participant = Participant.objects.create_user("Bob", password="1234", is_superuser=True)
        client.force_login(participant)
        response = client.get(reverse("demographics"))

        demographics_service.return_value = "foo"
        mock_statistics_service.return_value = "bar"

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/demographics.html")

    @patch('evaluationDashboard.views.import_questions')
    @skip
    def test_call_REST_API_import_script_no_superuser(self, import_questions_mock):
        client = Client()
        normal_participant = Participant.objects.create_user(username="Bob", password="iamgroot")
        client.force_login(normal_participant)

        response = client.get(reverse("import_script"))

        self.assertEqual(response.status_code, 403)

    @patch('evaluationDashboard.views.import_questions')
    @skip
    def test_call_REST_API_import_script_superuser(self, import_questions_mock):
        client = Client()
        normal_participant = Participant.objects.create_user(username="Bob", password="iamgroot", is_superuser=True)
        client.force_login(normal_participant)

        response = client.get(reverse("import_script"))

        self.assertEqual(response.status_code, 200)

    @patch('evaluationDashboard.views.import_questions')
    @skip
    def test_call_REST_API_import_script_function_is_called(self, import_questions_mock):
        client = Client()
        normal_participant = Participant.objects.create_user(username="Bob", password="iamgroot", is_superuser=True)
        client.force_login(normal_participant)

        response = client.get(reverse("import_script"))

        import_questions_mock.assert_called_once()
        self.assertEqual(response.status_code, 200)

    @patch('evaluationDashboard.views.EvaluationDataService.get_question_data')
    def test_download_answers(self, get_answer_data_mock):
        get_answer_data_mock.side_effect = []

        client = Client()
        no_superuser_participant = Participant.objects.create_user(username="Bob", password="Iamgroot", is_superuser=False)

        client.force_login(no_superuser_participant)

        response = client.get(reverse("download_evaluation_data"))

        self.assertEqual(response.status_code, 403)

    if __name__ == '__main__':
        unittest.main()
