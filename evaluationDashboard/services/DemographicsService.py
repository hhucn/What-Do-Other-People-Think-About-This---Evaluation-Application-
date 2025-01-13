from collections import Counter

from evaluation.models.Participant import Participant


class DemographicsService:
    @staticmethod
    def get_demographics():
        participants = Participant.objects.all()

        return {
            "gender": dict(Counter(p.gender for p in participants)),
            "age": dict(Counter(str(p.age)[0] + "0" for p in participants)),
            "education": dict(Counter(p.education for p in participants))
        }

    @staticmethod
    def get_demographics_data():
        participants = Participant.objects.all()
        demographics_data = []
        for participant in participants:
            demographics_data.append({"username": participant.username, "age": participant.age, "education": participant.education, "gender": participant.gender})
        return demographics_data
