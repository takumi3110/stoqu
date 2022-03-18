from rest_framework import serializers

from .models import QuoteItem


class QuoteItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteItem
        fields = ('id', 'number', 'item', 'quantity', 'registration_at', 'ordered_at', 'ordered', 'arrived_at',
                  'delivery_at', 'delivered', 'worker')
 