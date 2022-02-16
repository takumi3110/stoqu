from rest_framework import routers

from . import views

app_name = 'user'

router.register(r'base', views.BaseViewSet)
router.register(r'room', views.RoomViewSet)
router.register(r'requester', views.RequesterViewSet)
