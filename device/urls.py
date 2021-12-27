# -*- cording:utf-8 -*-

from django.urls import path
from rest_framework import routers

from . import views

app_name = 'device'

router = routers.DefaultRouter()
router.register(r'cpu', views.CPUViewSet)
router.register(r'storage', views.StorageViewSet)
router.register(r'pc', views.PCViewSet)
router.register(r'pcdetail', views.PCDetailViewSet)

urlpatterns = [
	path('createPC/', views.PCCreateView.as_view(), name='create_pc'),
	path('createPcDetail/', views.PCDetailCreateView.as_view(), name='create_pcdetail'),
	path('updatePcDetail/', views.PCDetailUpdateView.as_view(), name='update_pcdetail')
]
