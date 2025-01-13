from django.contrib.auth.forms import UserCreationForm
from django import forms

from evaluation.models import Participant

GENDER_CHOICES = {
    "male": "Male",
    "female": "Female",
    "divers": "Divers",
    "none": "None"
}

EDUCATION_CHOICES = {
    "bachelor": "Bachelor",
    "master": "Master",
    "phd": "Phd"
}

class ParticipantRegisterForm(UserCreationForm):
    class Meta:
        model = Participant
        fields = ['username', 'password1', 'password2']

    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    education = forms.ChoiceField(choices=EDUCATION_CHOICES)
    age = forms.IntegerField()
