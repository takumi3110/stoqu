from django.urls import path

from . import views

app_name = 'quote'

urlpatterns = [
    path('', views.genre_select, name='genre'),
    path('order/<str:genre>', views.quote_order, name='order')
]
