# -*- coding:utf-8 -*-

from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm

from .models import PCDetail, PC


class PCDetailCreateBSModalForm(BSModalModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'

	class Meta:
		model = PCDetail
		fields = ('category', 'maker', 'name', 'model_number', 'img')


class PCCreateBSModalForm(BSModalModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'

	class Meta:
		model = PC
		fields = ('pc', 'cpu', 'memory', 'storage', 'size', 'camera', 'fingerprint', 'numpad', 'lan', 'usb', 'hdmi', 'vga')
