# -*- cording:utf-8 -*-
from rest_framework import serializers

from .models import CPU, Storage, PCSpec, PC, Item


class CPUSerializer(serializers.ModelSerializer):
	class Meta:
		model = CPU
		fields = ('maker', 'name', 'gen')


class StorageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Storage
		fields = ('type', 'size')


class PCSpecSerializer(serializers.ModelSerializer):
	class Meta:
		model = PCSpec
		fields = ('cpu', 'memory', 'storage', 'size', 'camera', 'fingerprint', 'numpad', 'lan', 'usb', 'hdmi', 'vga')


class PCSerializer(serializers.ModelSerializer):
	class Meta:
		model = PC
		fields = ('category', 'maker', 'name', 'model_number')


class ItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = Item
		fields = ('pc', 'spec', 'remarks')
