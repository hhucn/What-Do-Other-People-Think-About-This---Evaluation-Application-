import unittest
from typing import Dict

from evaluation.models import Participant
from evaluation.models.Enums.Education import Education
from evaluation.models.Enums.Gender import Gender
from evaluationDashboard.services.DemographicsService import DemographicsService


class DemographicsServiceTests(unittest.TestCase):
    def setUp(self):
        self.participant_1 = Participant.objects.create_user(username="Alice", password="1234", age=20, education=Education.MASTER, gender=Gender.FEMALE)
        self.participant_2 = Participant.objects.create_user(username="Bob", password="1234", age=58, education=Education.BACHELOR, gender=Gender.DIVERS)
        self.participant_3 = Participant.objects.create_user(username="Charlie", password="1234", age=32, education=Education.MASTER, gender=Gender.MALE)
        self.participant_4 = Participant.objects.create_user(username="Daisy", password="1234", age=53, education=Education.MASTER, gender=Gender.FEMALE)
        self.participant_5 = Participant.objects.create_user(username="Edward", password="1234", age=40, education=Education.PHD, gender=Gender.NO_SELECTION)

    def tearDown(self):
        Participant.objects.all().delete()

    def test_get_demographics_age_data(self):
        demographics: Dict = DemographicsService.get_demographics()

        self.assertEqual(demographics["age"]["20"], 1)  # add assertion here
        self.assertEqual(demographics["age"]["30"], 1)  # add assertion here
        self.assertEqual(demographics["age"]["40"], 1)  # add assertion here
        self.assertEqual(demographics["age"]["50"], 2)  # add assertion here

    def test_get_demographics_gender_data(self):
        demographics = DemographicsService.get_demographics()

        self.assertEqual(demographics["gender"]["FEMALE"], 2)
        self.assertEqual(demographics["gender"]["MALE"], 1)
        self.assertEqual(demographics["gender"]["DIVERS"], 1)
        self.assertEqual(demographics["gender"]["NO_SELECTION"], 1)

    def test_get_demographics_education_data(self):
        demographics = DemographicsService.get_demographics()

        self.assertEqual(demographics["education"]["BACHELOR"], 1)
        self.assertEqual(demographics["education"]["MASTER"], 3)
        self.assertEqual(demographics["education"]["PHD"], 1)


if __name__ == '__main__':
    unittest.main()
