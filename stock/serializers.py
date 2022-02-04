from rest_framework import serializers

from .models import *
from device.serializer import PCDetailSerializer


class OptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Option
		fields = ('maker', 'name', 'price', 'quantity', 'remarks')


class BaseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Base
		fields = ('name',)


class KittingPlanSerializer(serializers.ModelSerializer):
	class Meta:
		model = KittingPlan
		fields = ('id', 'name', 'price')


class StorageItemSerializer(serializers.ModelSerializer):
	item = PCDetailSerializer()
	# option = OptionSerializer()
	base = BaseSerializer()

	class Meta:
		model = StorageItem
		fields = ('order_number', 'item', 'price', 'quantity', 'option', 'base', 'delivery_at', 'remarks')


class OrderItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderItem
		fields = ('id', 'storage_item', 'quantity', 'ordered', 'kitting_plan', 'requester')


class StorageCartSerializer(serializers.ModelSerializer):
	class Meta:
		model = StorageCart
		fields = ('requester', 'order_item', 'order_item')


class ApproveSerializer(serializers.ModelSerializer):
	class Meta:
		model = Approve
		fields = ('last_name', 'first_name', 'dept_code', 'dept_name')


class OrderInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderInfo
		fields = ('number', 'ticket', 'storage_cart', 'approve', 'requester', 'contact_user', 'ordered_at', 'ordered')
