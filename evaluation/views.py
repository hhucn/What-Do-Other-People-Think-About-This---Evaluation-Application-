import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from evaluation.applicationservice.EvaluationService import EvaluationService
from evaluation.domain.PointOfViewQuestion import PointOfViewQuestion
from evaluation.forms import ParticipantRegisterForm
from evaluation.models import Participant
from evaluation.models.AnswerRepository import AnswerRepository
from evaluation.models.ParticipantRepository import ParticipantRepository
from evaluation.models.QuestionRepository import QuestionRepository


def index(request):
    if request.user.is_authenticated:
        return redirect('question')
    else:
        return redirect('login')


def consent(request):
    return render(request, template_name='registration/consent.html')


def consent_declined(requests):
    return render(requests, template_name='registration/consent_declined.html')


def onboarding_tour(request):
    return render(request, template_name='evaluation/comment_question_onboarding_tour.html')


def onboarding_tour_comment_question_part_2(request):
    return render(request, template_name='evaluation/comment_question_onboarding_tour_part_2.html')


def onboarding_tour_comment_question_part_3(request):
    return render(request, template_name='evaluation/comment_question_onboarding_tour_part_3.html')


def onboarding_tour_point_of_view_question(request):
    return render(request, template_name='evaluation/point_of_view_question_onboarding_tour.html')


def register(request):
    if request.method == 'POST':
        form = ParticipantRegisterForm(request.POST)
        if form.is_valid():
            new_participant = Participant.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password1'],
                                                              gender=form.cleaned_data['gender'], education=form.cleaned_data['education'], age=form.cleaned_data['age'])
            login(request, new_participant)
            messages.success(request, "Welcome!")
            return redirect('onboarding_tour')
    else:
        form = ParticipantRegisterForm()
    return render(request, 'registration/registration.html', {'form': form})


def view_login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, "registration/login.html", {"form": form})
    elif request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {username}!")
                return redirect('question')
        else:
            messages.error(request, "Invalid username or password")
    return redirect('login')


def view_log_out(request):
    logout(request)
    return redirect('index')


def user_study_complete(request):
    return render(request, template_name="evaluation/user_study_complete.html")


class PointOfViewAnswerView(LoginRequiredMixin, View):

    def __init__(self, **kwargs):
        self.evaluation_service: EvaluationService = kwargs.get("evaluation_service", EvaluationService(QuestionRepository(), AnswerRepository(), ParticipantRepository()))

    def get(self, request, *args, **kwargs):
        try:
            self.evaluation_service.save_point_of_view_answer(participant_id=self.request.session.get("_auth_user_id"), question_id=kwargs.get("question_id"),
                                                              recommendation_method=kwargs.get("recommendation_method"), selected_method=kwargs.get("selected_method"))
        except IntegrityError:
            logging.error("Cannot store duplicate answers")
        return redirect('question')


class CommentAnswerView(LoginRequiredMixin, View):

    def __init__(self, **kwargs):
        self.evaluation_service: EvaluationService = kwargs.get("evaluation_service", EvaluationService(QuestionRepository(), AnswerRepository(), ParticipantRepository()))

    def get(self, request, *args, **kwargs):
        try:
            participant = self.evaluation_service.save_comment_answer(participant_id=self.request.session.get("_auth_user_id"), question_id=kwargs.get("question_id"),
                                                                      recommendation_method=kwargs.get("recommendation_method"),
                                                                      comment_id=kwargs.get("comment_id"), good_recommendation=kwargs.get("good_recommendation"))
            if participant.get_next_question() is None:
                print("Next question is None. Redirect to point of view question")
                return redirect(reverse('point-of-view-question', args=(self.kwargs.get("question_id"), kwargs.get("recommendation_method"))))
        except IntegrityError:
            logging.error("Cannot store duplicate answers")
        return redirect(reverse('comment-question', args=(self.kwargs.get("question_id"), self.kwargs.get("recommendation_method"))))


class QuestionView(LoginRequiredMixin, TemplateView):
    login_url = "/login/"
    template_name = "evaluation/comment_question.html"

    def __init__(self, *args, **kwargs):
        self.evaluation_service: EvaluationService = kwargs.get("evaluation_service", EvaluationService(QuestionRepository(), AnswerRepository(), ParticipantRepository()))

    def dispatch(self, request, *args, **kwargs):
        if self.evaluation_service is not None:
            participant = self.evaluation_service.get_participant_with_next_question(self.request.session.get("_auth_user_id"), None, None)
            if participant.get_next_question() is None and participant.progress == 100.0:
                return redirect(reverse("user-study-complete"))
            elif isinstance(participant.get_next_question(), PointOfViewQuestion):
                return redirect(reverse("point-of-view-question", args=(participant.get_next_question().question_id, participant.get_next_question().recommendation_method)))

            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.evaluation_service is not None:
            participant = self.evaluation_service.get_participant_with_next_question(self.request.session.get("_auth_user_id"), None, None)
            context["next_question"] = participant.get_next_question()
            context["progress"] = participant.get_progress()

        return context


class CommentQuestionView(LoginRequiredMixin, TemplateView):
    login_url = "/login/"
    template_name = "evaluation/comment_question.html"

    def __init__(self, *args, **kwargs):
        self.evaluation_service: EvaluationService = kwargs.get("evaluation_service", EvaluationService(QuestionRepository(), AnswerRepository(), ParticipantRepository()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.evaluation_service is not None:
            participant = self.evaluation_service.get_participant_with_next_question(self.request.session.get("_auth_user_id"), self.kwargs.get("question_id", None), self.kwargs.get("recommendation_method"))
            context["next_question"] = participant.get_next_question()
            context["progress"] = participant.get_progress()

        return context


class PointOfQuestionView(LoginRequiredMixin, TemplateView):
    login_url = "/login/"
    template_name = "evaluation/point_of_view_question.html"

    def __init__(self, *args, **kwargs):
        self.evaluation_service: EvaluationService = kwargs.get("evaluation_service", EvaluationService(QuestionRepository(), AnswerRepository(), ParticipantRepository()))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.evaluation_service is not None:
            participant = self.evaluation_service.get_participant_with_next_question(self.request.session.get("_auth_user_id"), self.kwargs.get("question_id", None), self.kwargs.get("recommendation_method", None))
            context["next_question"] = participant.get_next_question()
            context["progress"] = participant.get_progress()

        return context
