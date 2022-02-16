from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from bootstrap_modal_forms.generic import BSModalUpdateView
from rest_framework import viewsets

from .models import *
from .serializers import *
from .filters import *
from .forms import RequesterUpdateBsModalForm


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


class RequesterUpdateView(LoginRequiredMixin, BSModalUpdateView):
	model = Requester
	template_name = 'snippets/update_modal.html'
	form_class = RequesterUpdateBsModalForm
	success_url = reverse_lazy('stock:storage_list')
