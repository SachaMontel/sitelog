from django.urls import path
from . import views

app_name = 'annee'

urlpatterns = [
    path('', views.index, name='index'),
    path('gl/', views.gl, name='gl'),
    path('logout/', views.logout, name='logout'),
    # Ajoutez vos URLs ici
    # Exemple :
    # path('', views.index, name='index'),
]
