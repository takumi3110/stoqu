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
	cpu = CPUSerializer()
	storage = StorageSerializer()

	class Meta:
		model = PCSpec
		fields = ('cpu', 'memory', 'storage', 'size', 'camera', 'fingerprint', 'numpad', 'lan', 'usb', 'hdmi', 'vga')

	def create(self, validated_data):
		cpu_data_list = validated_data.pop('cpu')
		storage_data_list = validated_data.pop('storage')
		pc_spec = PCSpec.objects.create(**validated_data)
		for cpu_data in cpu_data_list:
			CPU.objects.create(pcspec=pc_spec, **cpu_data)
		for storage_data in storage_data_list:
			Storage.objects.create(pc_spec=pc_spec, **storage_data)
		return pc_spec


class PCSerializer(serializers.ModelSerializer):
	class Meta:
		model = PC
		fields = ('category', 'maker', 'name', 'model_number')


class ItemSerializer(serializers.ModelSerializer):
	pc = PCSerializer(read_only=True)
	spec = PCSpecSerializer(read_only=True)

	class Meta:
		model = Item
		fields = ('pc', 'spec', 'remarks')
