# -*- cording:utf-8 -*-

from django.urls import path
from rest_framework import routers

from . import views

app_name = 'stock'

router = routers.DefaultRouter()
router.register(r'option', views.OptionViewSet)
router.register(r'base', views.BaseViewSet)
router.register(r'storage', views.StorageItemViewSet)
router.register(r'orderItem', views.OrderItemViewSet)
router.register(r'storageCart', views.StorageCartViewSet)
router.register(r'approve', views.ApproveViewSet)
router.register(r'orderInfo', views.OrderInfoViewSet)

urlpatterns = [
	path('', views.StorageItemListView.as_view(), name='storage_list'),
	path('detail/<int:pk>', views.StorageItemDetailView.as_view(), name='storage_detail'),
	path('get_data/', views.create_storage_data, name='get_data'),
	path('create/', views.StorageItemCreateView.as_view(), name='storage_create'),
	path('update/<int:pk>', views.StorageItemUpdateView.as_view(), name='storage_update'),
	path('optionCreate/', views.OptionCreateView.as_view(), name='option_create')
]
