from django.urls import path;
from MiSalud import views;


urlpatterns = [
    path('', views.Inicio, name="Home"),
]
