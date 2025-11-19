from django.urls import path
from . import views

app_name = 'annee'

urlpatterns = [
    path('', views.index, name='index'),
    path('gl/', views.gl, name='gl'),
    path('logout/', views.logout, name='logout'),
    path('nathan/', views.wall, name='wall'),
    path('upload-photo/', views.upload_photo, name='upload_photo'),
    path('add-message/', views.add_message, name='add_message'),
]
