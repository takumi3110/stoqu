from django_filters import rest_framework as filters

from .models import QuoteItem, OrderItem, OrderInfo


class QuoteItemFilter(filters.FilterSet):
    class Meta:
        model = QuoteItem
        fields = ['number', 'item', 'worker', 'entered']


class OrderItemFilter(filters.FilterSet):
    class Meta:
        model = OrderItem
        fields = ['destination', 'quote_item', 'worker', 'ordered', 'arrived', 'delivered']


class OrderInfoFilter(filters.FilterSet):
    class Meta:
        model = OrderInfo
        fields = ['status', 'number', 'ticket', 'finished']
