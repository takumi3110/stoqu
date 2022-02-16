from rest_framework import serializers

from .models import *


class BaseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Base
		fields = ('name',)


class RoomSerializer(serializers.ModelSerializer):
	class Meta:
		model = Room
		fields = ('name', 'base')


class RequesterSerializer(serializers.ModelSerializer):
	class Meta:
		model = Requester
		fields = ('user', 'room')
