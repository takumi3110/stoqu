# -*- cording:utf-8 -*-
from rest_framework import serializers

from .models import CPU, Storage, PC, PCDetail


class CPUSerializer(serializers.ModelSerializer):
	class Meta:
		model = CPU
		fields = ('maker', 'name', 'gen')


class StorageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Storage
		fields = ('type', 'size')


class PCSerializer(serializers.ModelSerializer):
	class Meta:
		model = PC
		fields = ('category', 'maker', 'name', 'model_number')


class PCDetailSerializer(serializers.ModelSerializer):
	pc = PCSerializer(read_only=True)
	cpu = CPUSerializer(read_only=True)
	storage = StorageSerializer(read_only=True)

	class Meta:
		model = PCDetail
		fields = ('pc', 'cpu', 'memory', 'storage', 'size', 'camera', 'fingerprint', 'numpad', 'lan', 'usb', 'hdmi', 'vga', 'remarks')
