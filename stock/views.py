from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView

from rest_framework import viewsets
import openpyxl as px
import datetime

import device.models
from .models import Option, Base, StorageItem
from device.models import CPU, PCDetail, PC, Storage
from .serializer import OptionSerializer, BaseSerializer, StorageItemSerializer
from .forms import StorageItemBSModalForm, StorageItemUpdateBSModalForm, OptionCreateBSModalForm


class OptionViewSet(viewsets.ModelViewSet):
	queryset = Option.objects.all()
	serializer_class = OptionSerializer


class BaseViewSet(viewsets.ModelViewSet):
	queryset = Base.objects.all()
	serializer_class = BaseSerializer


class StorageItemViewSet(viewsets.ModelViewSet):
	queryset = StorageItem.objects.all()
	serializer_class = StorageItemSerializer


class StorageItemListView(LoginRequiredMixin, ListView):
	model = StorageItem
	template_name = 'stock/storage_list.html'
	paginate_by = 20
	ordering = 'order_number'

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super().get_context_data(**kwargs)
		base = Base.objects.all()
		context['base_list'] = base
		return context


class StorageItemDetailView(LoginRequiredMixin, DetailView):
	model = StorageItem
	template_name = 'stock/storage_detail.html'


class StorageItemCreateView(LoginRequiredMixin, BSModalCreateView):
	model = StorageItem
	template_name = 'snippets/create_modal.html'
	form_class = StorageItemBSModalForm
	success_url = reverse_lazy('stock:storage_list')


class StorageItemUpdateView(LoginRequiredMixin, BSModalUpdateView):
	model = StorageItem
	template_name = 'snippets/update_modal.html'
	form_class = StorageItemUpdateBSModalForm
	success_url = reverse_lazy('stock:storage_list')


class OptionCreateView(LoginRequiredMixin, BSModalCreateView):
	model = Option
	template_name = 'snippets/create_modal.html'
	form_class = OptionCreateBSModalForm
	success_url = reverse_lazy('stock:storage_list')


def create_storage_data(request):
	"""
	データ取り込み用
	:param request:
	:return:
	"""
	file = r'D:\Users\19020081\Documents\【貯蔵品】PC在庫リスト.xlsx'
	wb = px.load_workbook(file)
	ws = wb.worksheets[0]
	# max_row = ws.max_row
	max_row = 442
	for i in range(3, max_row):
		b_value = ws['B' + str(i)].value
		active = ws['C' + str(i)].value
		base = ws['E' + str(i)].value
		order_number = ws['F' + str(i)].value
		date = ws['G' + str(i)].value
		item_name = ws['H' + str(i)].value
		model_number = ws['I' + str(i)].value
		price = int(ws['K' + str(i)].value)
		remarks = ws['L' + str(i)].value
		# delivery_date
		delivery_date = date.date().isoformat()
		# category, numpad
		category_numpad_size = get_category_and_numpad_and_size(b_value)
		category = category_numpad_size['category']
		numpad = category_numpad_size['numpad']
		size = category_numpad_size['size']
		# maker, name
		split_name = item_name.split(' ')
		maker = ''
		name = ''
		for n in range(len(split_name)):
			if n == 0:
				maker = split_name[n]
			else:
				name += split_name[n]
		if active == '空':
			pc = PC.objects.get_or_create(
				category=category,
				maker=maker,
				name=name,
				model_number=model_number
			)
			pc_detail = PCDetail.objects.get_or_create(
				pc=pc[0],
				cpu_id=1,
				storage_id=2,
				size=size,
				numpad=numpad,
			)
			get_base = Base.objects.get_or_create(
				name=base
			)

			stock_storage, create_storage = StorageItem.objects.get_or_create(
				order_number=order_number,
				item=pc_detail[0],
				price=price,
				base=get_base[0],
				delivery_date=delivery_date,
			)
			if create_storage:
				stock_storage.quantity = 1
			else:
				stock_storage.quantity += 1
			stock_storage.remarks = remarks
			stock_storage.save()
	return redirect('stock:storage_list')


def get_category_and_numpad_and_size(value):
	"""
	categoryを分別する
	:param value:
	:return category_and_numpad_and_size:
	"""
	category_and_numpad_and_size = {
		'size': None
	}
	if 'ノート' in value:
		category_and_numpad_and_size['category'] = '1'
		if 'B5' in value:
			category_and_numpad_and_size['numpad'] = False
			category_and_numpad_and_size['size'] = 13
		elif 'A4' in value:
			category_and_numpad_and_size['numpad'] = True
			category_and_numpad_and_size['size'] = 15
	elif '小型' in value:
		category_and_numpad_and_size['category'] = '3'
		category_and_numpad_and_size['numpad'] = False
	return category_and_numpad_and_size
