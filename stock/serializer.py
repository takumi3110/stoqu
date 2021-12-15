# -*- cording:utf-8 -*-

from rest_framework import serializers

from .models import Option, Base, Storage


class OptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Option
		fields = ('maker', 'name', 'price', 'quantity', 'remarks')


class BaseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Base
		fields = ('name',)


class StorageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Storage
		fields = ('order_number', 'item', 'price', 'quantity', 'option', 'base', 'remarks')
