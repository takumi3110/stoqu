from django.shortcuts import render

from rest_framework import viewsets

from .models import *
from .serializers import *
from .filters import *


class BaseViewSet(viewsets.ModelViewSet):
	queryset = Base.objects.all()
	serializer_class = BaseSerializer
	filter_class = BaseFilter


class RoomViewSet(viewsets.ModelViewSet):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer
	filter_class = RoomFilter


class RequesterViewSet(viewsets.ModelViewSet):
	queryset = Requester.objects.all()
	serializer_class = RequesterSerializer
	filter_class = RequesterFilter
