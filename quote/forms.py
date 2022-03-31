from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm

from .models import Destination


class DestinationCreateBSModalForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(DestinationCreateBSModalForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = Destination
        fields = ('name',)
