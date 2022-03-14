from django.urls import path

from . import views

app_name = 'quote'

urlpatterns = [
    path('', views.genre_select, name='genre')
]
