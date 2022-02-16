from django import forms
from bootstrap_modal_forms.forms import BSModalForm

from .models import Requester


class RequesterUpdateBsModalForm(BSModalForm):
	def __init__(self, *args, **kwargs):
		super(RequesterUpdateBsModalForm, self).__init__(*args, **kwargs)
		for field in self.fields.values():
			field.widget.attrs['class'] = 'form-control'
		self.fields['user'].widget.attrs['readonly'] = True

	class Meta:
		model = Requester
		fields = ('user', 'room')
