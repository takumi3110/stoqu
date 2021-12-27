# -*- cording:utf-8 -*-

from django.urls import path
from rest_framework import routers

from . import views

app_name = 'device'

router = routers.DefaultRouter()
router.register(r'cpu', views.CPUViewSet)
router.register(r'storage', views.StorageViewSet)
router.register(r'pc', views.PCDetailViewSet)
router.register(r'item', views.PCViewSet)

urlpatterns = [
	path('createPC/', views.PCDetailCreateView.as_view(), name='create_pcdetail'),
	path('createItem/', views.PCCreateView.as_view(), name='create_pc')
]
