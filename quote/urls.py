from django.urls import path
from rest_framework import routers

from . import views

app_name = 'quote'

router = routers.DefaultRouter()
router.register(r'quoteItem', views.QuoteItemViewSet)

urlpatterns = [
    path('', views.genre_select, name='genre'),
    path('order/<str:genre>', views.quote_order, name='order'),
    path('item_list/', views.QuoteItemList.as_view(), name='item_list'),
    path('delete_item/<int:pk>', views.delete_quote_item, name='delete_item')
]
