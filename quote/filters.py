from django_filters import rest_framework as filters

from .models import QuoteItem


class QuoteItemFilter(filters.FilterSet):
    class Meta:
        model = QuoteItem
        fields = ['number', 'item', 'worker', 'ordered']
