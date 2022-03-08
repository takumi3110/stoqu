from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm

from .models import Option, StorageItem, Approve, OrderInfo


class StorageItemBSModalForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = StorageItem
        fields = ('order_number', 'item', 'price', 'quantity', 'option', 'base', 'registration_at', 'remarks')


class StorageItemUpdateBSModalForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].widget.attrs['readonly'] = 'readonly'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = StorageItem
        fields = ('order_number', 'item', 'price', 'quantity', 'option', 'base', 'registration_at', 'remarks')


class OptionCreateBSModalForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = Option
        fields = ('maker', 'name', 'price', 'quantity', 'remarks')


class ApproveBSModalForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(ApproveBSModalForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['requester'].initial = kwargs['request'].user
    
    # self.fields['requester'].widget.attrs['disabled'] = True
    
    class Meta:
        model = Approve
        fields = ('last_name', 'first_name', 'dept_code', 'dept_name', 'requester')


class OrderInfoBSModalForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderInfoBSModalForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['number'].widget.attrs['readonly'] = 'readonly'
    
    class Meta:
        model = OrderInfo
        fields = ('number', 'ticket', 'contact_user')
