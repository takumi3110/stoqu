from django.urls import path
from rest_framework import routers

from . import views

app_name = 'user'

router = routers.DefaultRouter()
router.register(r'base', views.BaseViewSet)
router.register(r'room', views.RoomViewSet)
router.register(r'requester', views.RequesterViewSet)

urlpatterns = [
	path('requester/<int:pk>', views.RequesterUpdateView.as_view(), name='requester_update')
]
