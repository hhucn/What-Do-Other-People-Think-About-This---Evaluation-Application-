from django.urls import path

from evaluationDashboard import views

urlpatterns = [
    path('', views.index, name='dashboard_index'),
    path('demographics', views.demographics, name='demographics'),
    path('download_evaluation_data', views.download_evaluation_data, name='download_evaluation_data'),
    # path('import_script', views.import_script, name='import_script'),
]
