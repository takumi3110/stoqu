from django.urls import path
from rest_framework import routers

from . import views

app_name = 'quote'

router = routers.DefaultRouter()
router.register(r'quoteItem', views.QuoteItemViewSet)
router.register(r'orderItem', views.OrderItemViewSet)
router.register(r'orderInfo', views.OrderInfoViewSet)

urlpatterns = [
    path('', views.genre_select, name='genre'),
    path('order/<str:genre>', views.quote_order, name='order'),
    path('item_list/', views.QuoteItemList.as_view(), name='item_list'),
    path('delete_item/<int:pk>', views.delete_quote_item, name='delete_item'),
    path('register_destination/', views.register_destination, name='register_destination'),
    path('add_destination/', views.AddDestination.as_view(), name='add_destination'),
    path('add_requester/', views.add_requester, name='add_requester'),
    path('create_pdf/<int:pk>', views.AllCreatePdf.as_view(), name='create_pdf'),
    path('orderinfo/', views.OrderInfoView.as_view(), name='orderinfo'),
    path('mypage/', views.OrderInfoMyView.as_view(), name='mypage'),
    path('orderinfo_detail/<int:pk>', views.OrderInfoDetailView.as_view(), name='orderinfo_detail')
]
