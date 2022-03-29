from rest_framework import serializers

from .models import QuoteItem, OrderItem, OrderInfo


class QuoteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteItem
        fields = ('id', 'number', 'item', 'quantity', 'registration_at', 'ordered', 'worker')


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'destination', 'quote_item', 'ordered', 'ordered_at', 'arrived', 'arrived_at', 'delivered',
                  'delivery_at')


class OrderInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderInfo
        fields = ('id', 'status', 'number', 'ticket', 'cart', 'registration_at', 'updated_at', 'finished',
                  'finished_at')
