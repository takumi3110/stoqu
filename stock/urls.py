# -*- cording:utf-8 -*-

from django.urls import path
from rest_framework import routers

from . import views

app_name = 'stock'

router = routers.DefaultRouter()
router.register(r'option', views.OptionViewSet)
router.register(r'base', views.BaseViewSet)
router.register(r'storage', views.StorageViewSet)

urlpatterns = [
	path('', views.StorageListView.as_view(), name='storage_list'),
	path('detail/<int:pk>', views.StorageDetailView.as_view(), name='storage_detail'),
	path('get_data/', views.create_storage_data, name='get_data'),
]
