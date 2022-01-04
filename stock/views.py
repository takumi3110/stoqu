from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView

from rest_framework import viewsets
import openpyxl as px
import datetime

import device.models
from .models import Option, Base, StorageItem
from device.models import CPU, PCDetail, PC, Storage
from .serializer import *
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


class StorageCartViewSet(viewsets.ModelViewSet):
	queryset = StorageCart.objects.all()
	serializer_class = StorageCartSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
	queryset = OrderItem.objects.all()
	serializer_class = OrderItemSerializer


class ApproveViewSet(viewsets.ModelViewSet):
	queryset = Approve.objects.all()
	serializer_class = ApproveSerializer


class OrderInfoViewSet(viewsets.ModelViewSet):
	queryset = OrderInfo.objects.all()
	serializer_class = OrderInfoSerializer


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


def get_obj(resource, request, pk):
	"""

	:param resource:
	:param request:
	:param pk:
	:return:
	"""
	cart_list = StorageCart.objects.filter(requester=request.user, ordered=False)
	if resource == 'add':
		item = get_object_or_404(StorageItem, pk=pk)
		order_item, created = OrderItem.objects.get_or_create(
			storage_item=item,
			ordered=False
		)
	else:
		order_item = get_object_or_404(OrderItem, pk=pk)
	obj_data = {
		'cart_list': cart_list,
		'order_item': order_item
	}
	return obj_data


class StorageCartListView(LoginRequiredMixin, ListView):
	model = StorageCart
	template_name = 'stock/cart_list.html'

	def get_queryset(self, **kwargs):
		queryset = super(StorageCartListView, self).get_queryset()
		qs = queryset.filter(requester=self.request.user, ordered=False)
		return qs


@login_required()
def add_item(request, pk):
	"""
	カートにアイテムを追加する
	:param request:
	:param pk:
	:return:
	"""
	obj_data = get_obj('add', request, pk)
	order_item = obj_data['order_item']
	cart_list = obj_data['cart_list']
	storage_quantity = order_item.storage_item.quantity
	if storage_quantity > 0:
		order_item.storage_item.quantity -= 1
		order_item.storage_item.save()
		for option in order_item.storage_item.option.all():
			option.quantity -= 1
			option.save()
	else:
		return redirect('stock:cart')
	if cart_list.exists():
		storage_cart = cart_list[0]
		if storage_cart.order_item.filter(order_item__pk=order_item.pk).exists():
			order_item.quantity += 1
			order_item.save()
		else:
			storage_cart.order_item.add(order_item)
	else:
		storage_cart = StorageCart.objects.create(
			requester=request.user,
		)
		storage_cart.order_item.add(order_item)
	return redirect('stock:cart')


@login_required()
def reduce_cart(request, pk):
	"""
	カートからアイテムを減らす
	:param request:
	:param pk:
	:return:
	"""
	obj_data = get_obj('reduce', request, pk)
	order_item = obj_data['order_item']
	cart_list = obj_data['cart_list']
	if cart_list.exists():
		order_item.storage_item.quantity += 1
		order_item.storage_item.save()
		for option in order_item.storage_item.option.all():
			option.quantity += 1
			option.save()
		if order_item.quantityu > 1:
			order_item.quantity -= 1
			order_item.save()
		else:
			order_item.delete()
	else:
		pass
	return redirect('stock:cart')


@login_required()
def remove_cart(request, pk):
	"""
	カートからアイテムを削除する
	:param request:
	:param pk:
	:return:
	"""
	obj_data = get_obj('remove', request, pk)
	order_item = obj_data['order_item']
	cart_list = obj_data['cart_list']
	if cart_list.exists():
		quantity = order_item.quantity
		order_item.storage_item.quantity += quantity
		order_item.storage_item.save()
		for option in order_item.storage_item.option.all():
			option.quantity += quantity
			option.save()
		for cart in cart_list:
			cart_items = cart.order_item.all().count()
			if cart_items == 1:
				cart.delete()
				order_item.delete()
			else:
				order_item.delete()
	else:
		pass
	return redirect('stock:cart')
