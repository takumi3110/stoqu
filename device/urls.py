# -*- cording:utf-8 -*-

from django.urls import path
from rest_framework import routers

from . import views

app_name = 'device'

router = routers.DefaultRouter()
router.register(r'cpu', views.CPUViewSet)
router.register(r'storage', views.StorageViewSet)
router.register(r'pc_spec', views.PCSpecViewSet)
router.register(r'pc', views.PCViewSet)
router.register(r'item', views.ItemViewSet)
