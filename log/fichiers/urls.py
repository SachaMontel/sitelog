from django.urls import path
from .views import upload_excel

app_name = "fichiers"

urlpatterns = [
    path('upload/', upload_excel, name='upload_excel'),
]