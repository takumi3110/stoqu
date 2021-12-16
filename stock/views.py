from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

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


class StorageListView(LoginRequiredMixin, ListView):
	model = Storage
	template_name = 'stock/storage_list.html'
	paginate_by = 20

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		base = Base.objects.all()
		context['base_list'] = base
		return context


class StorageDetailView(LoginRequiredMixin, DetailView):
	model = Storage
	template_name = 'stock/storage_detail.html'
