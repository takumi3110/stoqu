from django.shortcuts import render
from rest_framework import viewsets

from .models import Option, Base, Storage
from .serializer import OptionSerializer, BaseSerializer, StorageSerializer


class OptionViewSet(viewsets.ModelViewSet):
	queryset = Option.objects.all()
	serializer_class = OptionSerializer


class BaseViewSet(viewsets.ModelViewSet):
	queryset = Base.objects.all()
	serializer_class = BaseSerializer


class StorageViewSet(viewsets.ModelViewSet):
	queryset = Storage.objects.all()
	serializer_class = StorageSerializer
