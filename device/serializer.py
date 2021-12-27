# -*- cording:utf-8 -*-
from rest_framework import serializers

from .models import CPU, Storage, PCDetail, PC


class CPUSerializer(serializers.ModelSerializer):
	class Meta:
		model = CPU
		fields = ('maker', 'name', 'gen')


class StorageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Storage
		fields = ('type', 'size')


class PCDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = PCDetail
		fields = ('category', 'maker', 'name', 'model_number')


class PCSerializer(serializers.ModelSerializer):
	pc = PCDetailSerializer(read_only=True)
	cpu = CPUSerializer(read_only=True)
	storage = StorageSerializer(read_only=True)

	class Meta:
		model = PC
		fields = ('pc', 'cpu', 'memory', 'storage', 'size', 'camera', 'fingerprint', 'numpad', 'lan', 'usb', 'hdmi', 'vga', 'remarks')
