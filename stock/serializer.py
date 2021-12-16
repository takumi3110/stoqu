# -*- cording:utf-8 -*-

from rest_framework import serializers

from .models import Option, Base, Storage
from device.serializer import ItemSerializer


class OptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Option
		fields = ('maker', 'name', 'price', 'quantity', 'remarks')


class BaseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Base
		fields = ('name',)


class StorageSerializer(serializers.ModelSerializer):
	item = ItemSerializer()
	option = OptionSerializer()
	base = BaseSerializer()

	class Meta:
		model = Storage
		fields = ('order_number', 'item', 'price', 'quantity', 'option', 'base', 'delivery_date', 'remarks')
