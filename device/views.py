from django.shortcuts import render
from rest_framework import viewsets, filters
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView

from .models import CPU, Storage, PC, PCDetail
from .serializer import CPUSerializer, StorageSerializer, PCDetailSerializer, PCSerializer
from .forms import PCCreateBSModalForm, PCDetailCreateBSModalForm, PCDetailUpdateBSModalForm


class CPUViewSet(viewsets.ModelViewSet):
	queryset = CPU.objects.all()
	serializer_class = CPUSerializer


class StorageViewSet(viewsets.ModelViewSet):
	queryset = Storage.objects.all()
	serializer_class = StorageSerializer


class PCViewSet(viewsets.ModelViewSet):
	queryset = PC.objects.all()
	serializer_class = PCDetailSerializer


class PCDetailViewSet(viewsets.ModelViewSet):
	queryset = PCDetail.objects.all()
	serializer_class = PCSerializer


class PCCreateView(LoginRequiredMixin, BSModalCreateView):
	model = PC
	template_name = 'snippets/create_modal.html'
	form_class = PCCreateBSModalForm
	success_url = reverse_lazy('stock:storage_list')


class PCDetailCreateView(LoginRequiredMixin, BSModalCreateView):
	model = PCDetail
	template_name = 'snippets/create_modal.html'
	form_class = PCDetailCreateBSModalForm
	success_url = reverse_lazy('stock:storage_list')


class PCDetailUpdateView(LoginRequiredMixin, BSModalUpdateView):
	model = PCDetail
	template_name = 'snippets/update_modal.html'
	form_class = PCDetailUpdateBSModalForm
	success_url = reverse_lazy('stock:storage_list')
