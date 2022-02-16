from django_filters import rest_framework as filters

from .models import *


class BaseFilter(filters.FilterSet):
	class Meta:
		model = Base
		fields = ['name']


class RoomFilter(filters.FilterSet):
	class Meta:
		model = Room
		fields = ['name', 'base__name']


class RequesterFilter(filters.FilterSet):
	class Meta:
		model = Reuqester
		fields = ['user__username', 'room__name']
