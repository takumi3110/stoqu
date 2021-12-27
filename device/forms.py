# -*- coding:utf-8 -*-

from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm

from .models import PC,  PCDetail


class PCCreateBSModalForm(BSModalModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'

	class Meta:
		model = PC
		fields = ('category', 'maker', 'name', 'model_number', 'img')


class PCDetailCreateBSModalForm(BSModalModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'

	class Meta:
		model = PCDetail
		fields = ('pc', 'cpu', 'memory', 'storage', 'size', 'camera', 'fingerprint', 'numpad', 'lan', 'usb', 'hdmi', 'vga')


class PCDetailUpdateBSModalForm(BSModalModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['pc'].widget.attrs['disabled'] = 'disabled'
		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'

	class Meta:
		model = PCDetail
		fields = ('pc', 'cpu', 'memory', 'storage', 'size', 'camera', 'fingerprint', 'numpad', 'lan', 'usb', 'hdmi', 'vga')
