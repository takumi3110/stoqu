from django_filters import rest_framework as filters

from .models import *


class MyOrderingFilter(filters.OrderingFilter):
	descending_fmt = '%s (降順)'


class OptionFilter(filters.FilterSet):
	class Meta:
		model = Option
		fields = ['maker', 'name']


class BaseFilter(filters.FilterSet):
	class Meta:
		model = Base
		fields = ['name']


class StorageItemFilter(filters.FilterSet):
	class Meta:
		model = StorageItem
		fields = ['order_number', 'item__pc__name']


class KittingPlanFilter(filters.FilterSet):
	class Meta:
		model = KittingPlan
		fields = ['name']


class OrderItemFilter(filters.FilterSet):
	class Meta:
		model = OrderItem
		fields = ['storage_item__order_number', 'kitting_plan__name', 'requester__username']


class StorageCartFilter(filters.FilterSet):
	class Meta:
		model = StorageCart
		fields = ['requester__username', 'ordered']


class ApproveFilter(filters.FilterSet):
	class Meta:
		model = Approve
		fields = ['last_name', 'first_name', 'dept_code', 'dept_name', 'requester__username']


class OrderInfoFilter(filters.FilterSet):
	class Meta:
		model = OrderInfo
		fields = ['number', 'ticket', 'requester__username', 'contact_user__username', 'ordered']
