import csv
import io
import logging
import zipfile
from threading import Thread

import pandas
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseServerError
from django.shortcuts import render

from dbimport.import_evaluation_data import import_questions
from evaluationDashboard.services.DemographicsService import DemographicsService
from evaluationDashboard.services.EvaluationDataService import EvaluationDataService
from evaluationDashboard.services.StatisticsService import StatisticsService


def index(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")

    return render(request, "dashboard/statistics.html",
                  {"demographics": DemographicsService.get_demographics(),
                   "statistics": StatisticsService.get_statistics()})


def demographics(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")

    return render(request, "dashboard/demographics.html", {"demographics": DemographicsService.get_demographics(),
                                                           "statistics": StatisticsService.get_statistics()})


def import_script(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")

    try:
        thread = Thread(target=import_questions, daemon=True)
        thread.start()
        logging.info("Import of questions completed")
    except Exception as e:
        return HttpResponseServerError(e)

    return HttpResponse("Import started")


def download_evaluation_data(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You don't have permission to access this page.")

    question_data = EvaluationDataService.get_question_data()
    comment_selection_data = EvaluationDataService.get_comment_selections()
    comment_data = EvaluationDataService.get_comments()
    comment_answer_data = EvaluationDataService.get_comment_answers()
    point_of_view_answer_data = EvaluationDataService.get_point_of_view_answer_data()
    participant_data = EvaluationDataService.get_participant_data()

    evaluation_data = [
        ("question_data.csv", question_data),
        ("comment_selection_data.csv", comment_selection_data),
        ("comment_data.csv", comment_data),
        ("comment_answer_data.csv", comment_answer_data),
        ("point_of_view_answer_data.csv", point_of_view_answer_data),
        ("participant_data.csv", participant_data)
    ]

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:

        for filename, data in evaluation_data:
            csv_buffer = io.StringIO()
            pandas.DataFrame(data).to_csv(csv_buffer)
            zip_file.writestr(filename, csv_buffer.getvalue())

    zip_buffer.seek(0)

    response = HttpResponse(zip_buffer.getvalue(), content_type='application/x-zip')

    response['Content-Disposition'] = 'attachment; filename="evaluation_data.zip"'

    return response
