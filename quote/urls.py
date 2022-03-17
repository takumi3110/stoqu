from django.urls import path

from . import views

app_name = 'quote'

urlpatterns = [
    path('', views.genre_select, name='genre'),
    path('order/<str:genre>', views.quote_order, name='order'),
    path('item_list/', views.QuoteItemList.as_view(), name='item_list')
]
