# -*- coding:utf-8 -*-

from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm

from .models import Storage, Option


class StorageCreateBSModalForm(BSModalModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'

	class Meta:
		model = Storage
		fields = ('order_number', 'item', 'price', 'quantity', 'option', 'base', 'delivery_date', 'remarks')


class StorageUpdateBSModalForm(BSModalModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'

	class Meta:
		model = Storage
		fields = ('order_number', 'item', 'price', 'quantity', 'option', 'base', 'delivery_date', 'remarks')


class OptionCreateBSModalForm(BSModalModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'

	class Meta:
		model = Option
		fields = ('maker', 'name', 'price', 'quantity', 'remarks')
