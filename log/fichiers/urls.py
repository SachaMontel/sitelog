from django.urls import path
from .views import upload_excel, progression_export, telecharger_export

app_name = "fichiers"

urlpatterns = [
    path('upload/', upload_excel, name='upload_excel'),
    path('upload/progress/<str:job_id>/', progression_export, name='progression_export'),
    path('upload/download/<str:job_id>/', telecharger_export, name='telecharger_export'),
]
