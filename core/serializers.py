from django.forms import widgets
from rest_framework import serializers
from core.models import HealthyBee

class HealthyBeeSerializer(serializers.Serializer):
	pk = serializers.IntegerField(read_only=True)
	name = serializers.CharField(required=False, allow_blank=True)
	email = serializers.CharField(required=True)

	def create(self, data):
		return HealthyBee.objects.create(data)

class HealthyHiveSerializer(serializers.Serializer):
	pk = serializers.IntegerField(read_only=True)

class HealthDataSerializer(serializers.Serializer):
	bee = serializers.IntegerField(read_only=True)
	startTime = serializers.IntegerField(required=False)
	endTime = serializers.IntegerField(required=False)
	dataTypeName = serializers.CharField(required=False)
	originalDataSourceId = serializers.CharField(required=False)
	intVal = serializers.IntegerField(required=False)
	modifiedTime = serializers.IntegerField(required=False)
