from django.db import models

class HealthyBee(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    lastSyncTime = models.IntegerField(null=True)

class HealthyBeeAuth(models.Model):
    bee = models.ForeignKey('core.HealthyBee')
    token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200, null=True)

class HealthyHive(models.Model):
	name = models.CharField(max_length=200)

class HealthData(models.Model):
    bee = models.ForeignKey('core.HealthyBee', null=True)
    startTime = models.IntegerField(null=True)
    endTime = models.IntegerField(null=True)
    dataTypeName = models.CharField(max_length=256, null=True)
    originalDataSourceId = models.CharField(max_length=256, null=True)
    intVal = models.IntegerField(null=True)
    modifiedTime = models.IntegerField(null=True)

