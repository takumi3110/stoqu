from django.shortcuts import render
from rest_framework import viewsets, filters
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView

from .models import CPU, Storage, PCDetail, PC
from .serializer import CPUSerializer, StorageSerializer, PCDetailSerializer, PCSerializer
from .forms import PCDetailCreateBSModalForm, PCCreateBSModalForm


class CPUViewSet(viewsets.ModelViewSet):
	queryset = CPU.objects.all()
	serializer_class = CPUSerializer


class StorageViewSet(viewsets.ModelViewSet):
	queryset = Storage.objects.all()
	serializer_class = StorageSerializer


class PCDetailViewSet(viewsets.ModelViewSet):
	queryset = PCDetail.objects.all()
	serializer_class = PCDetailSerializer


class PCViewSet(viewsets.ModelViewSet):
	queryset = PC.objects.all()
	serializer_class = PCSerializer


class PCDetailCreateView(LoginRequiredMixin, BSModalCreateView):
	model = PCDetail
	template_name = 'snippets/create_modal.html'
	form_class = PCDetailCreateBSModalForm
	success_url = reverse_lazy('stock:storage_list')


class PCCreateView(LoginRequiredMixin, BSModalCreateView):
	model = PC
	template_name = 'snippets/create_modal.html'
	form_class = PCCreateBSModalForm
	success_url = reverse_lazy('stock:storage_list')
