from django.urls import path

from . import views
from .views import QuestionView, CommentQuestionView, PointOfQuestionView

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.view_login, name="login"),
    path("logout", views.view_log_out, name="logout"),
    path("question", QuestionView.as_view(), name="question"),
    path("comment-question/<int:question_id>/<str:recommendation_method>", CommentQuestionView.as_view(), name="comment-question"),
    path("point-of-view-question/<int:question_id>/<str:recommendation_method>", PointOfQuestionView.as_view(), name="point-of-view-question"),
    path("point-of-view-answer/<int:question_id>/<str:selected_method>/<str:recommendation_method>", views.PointOfViewAnswerView.as_view(), name='point-of-view-answer'),
    path("comment-answer/<int:question_id>/<str:recommendation_method>/<int:comment_id>/<str:good_recommendation>", views.CommentAnswerView.as_view(), name='comment-answer'),
    path("registration", views.register, name='registration'),
    path("log-out", views.view_log_out, name='logout'),
    path("consent", views.consent, name='consent'),
    path("consent-declined", views.consent_declined, name='consent_declined'),
    path("onboarding", views.onboarding_tour, name='onboarding_tour'),
    path("onboarding_comment_question_part_2", views.onboarding_tour_comment_question_part_2, name='onboarding_tour_comment_question_part_2'),
    path("onboarding_comment_question_part_3", views.onboarding_tour_comment_question_part_3, name='onboarding_tour_comment_question_part_3'),
    path("onboarding_point_of_view_question", views.onboarding_tour_point_of_view_question, name='onboarding_point_of_view_question'),
    path("user-study-complete", views.user_study_complete, name='user-study-complete'),
]
