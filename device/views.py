from django.shortcuts import render
from rest_framework import viewsets

from .models import CPU, Storage, PCSpec, PC, Item
from .serializer import CPUSerializer, StorageSerializer, PCSpecSerializer, PCSerializer, ItemSerializer


class CPUViewSet(viewsets.ModelViewSet):
	queryset = CPU.objects.all()
	serializer_class = CPUSerializer


class StorageViewSet(viewsets.ModelViewSet):
	queryset = Storage.objects.all()
	serializer_class = StorageSerializer


class PCSpecViewSet(viewsets.ModelViewSet):
	queryset = PCSpec.objects.all()
	serializer_class = PCSpecSerializer


class PCViewSet(viewsets.ModelViewSet):
	queryset = PC.objects.all()
	serializer_class = PCSerializer


class ItemViewSet(viewsets.ModelViewSet):
	queryset = Item.objects.all()
	serializer_class = ItemSerializer
