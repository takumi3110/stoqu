# -*- cording:utf-8 -*-

from rest_framework import serializers

from .models import Option, Base, StorageItem
from device.serializer import PCSerializer


class OptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Option
		fields = ('maker', 'name', 'price', 'quantity', 'remarks')


class BaseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Base
		fields = ('name',)


class StorageItemSerializer(serializers.ModelSerializer):
	item = PCSerializer()
	# option = OptionSerializer()
	base = BaseSerializer()

	class Meta:
		model = StorageItem
		fields = ('order_number', 'item', 'price', 'quantity', 'option', 'base', 'delivery_date', 'remarks')
