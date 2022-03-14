from django.urls import path

from . import views

app_name = 'quote'

url_patterns = [
    path('', views.genre_select, name='genre')
]
