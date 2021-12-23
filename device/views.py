from django.shortcuts import render
from rest_framework import viewsets, filters
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView

from .models import CPU, Storage, PCSpec, PC, Item
from .serializer import CPUSerializer, StorageSerializer, PCSpecSerializer, PCSerializer, ItemSerializer
from .forms import PCCreateBSModalForm, PCSpecCreateBSModalForm, ItemBSModalForm


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


class PCCreateView(LoginRequiredMixin, BSModalCreateView):
	model = PC
	template_name = 'snippets/create_modal.html'
	form_class = PCCreateBSModalForm
	success_url = reverse_lazy('stock:storage_list')


class PCSpecCreateView(LoginRequiredMixin, BSModalCreateView):
	model = PCSpec
	template_name = 'snippets/create_modal.html'
	form_class = PCSpecCreateBSModalForm
	success_url = reverse_lazy('stock:storage_list')


class ItemCreateView(LoginRequiredMixin, BSModalCreateView):
	model = Item
	template_name = 'snippets/create_modal.html'
	form_class = ItemBSModalForm
	success_url = reverse_lazy('stock:storage_list')
