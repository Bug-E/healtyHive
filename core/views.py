from django.http import HttpResponse, HttpResponseBadRequest
import json
from django.shortcuts import get_object_or_404
from core.models import HealthyBee, HealthyBeeAuth, HealthData
from core.serializers import HealthyBeeSerializer, HealthDataSerializer
from googleauth.views import getRequestUrl
from django.db.models import Sum

AVAILABLE_HEALTH_DATA_TYPES = ['com.google.weight', 'com.google.height', 'com.google.step_count.delta',
							'com.google.distance.delta']

def index(request):
	return HttpResponse('Be healthy!!');

def addUser(request):
	if request.method != 'POST':
		return get_object_or_404(HealthyBee)
	hb = HealthyBee(name = request.POST['name'], email = request.POST['email']);
	hb.save()
	return HttpResponse(json.dumps(HealthyBeeSerializer(hb).data))

def getAuthorizationUrl(request):
	if request.method != 'GET':
		return HttpResponseBadRequest('Invalid Method')
	if request.GET.get('bee_id') is None:
		return HttpResponseBadRequest('missing param: bee_id')
	url = getRequestUrl(request.GET['bee_id'])
	return HttpResponse(url)

def isAuthorized(request):
	if request.method != 'GET':
		return HttpResponseBadRequest('Invalid Method')
	if not request.GET.get('bee_id'):
		return HttpResponseBadRequest('missing param: bee_id')
	bee_id = request.GET.get('bee_id')
	hb = get_object_or_404(HealthyBee, pk=bee_id)
	hba = HealthyBeeAuth.objects.filter(bee=hb)
	authorized = False
	if hba:
		authorized = True
	return HttpResponse(json.dumps({'authorized' : authorized}))

def getAggregatedHealthData(request):
	if request.method != 'GET':
		return HttpResponseBadRequest('Invalid request method. Must be GET')
	dataType = request.GET.get('datatype')
	startTime = request.GET.get('starttime')
	endTime = request.GET.get('endTime')
	if dataType is None or startTime is None or endTime is None:
		return HttpResponseBadRequest('Invalid parameters. must contain datatype, starttime, endtime')
	if dataType not in AVAILABLE_HEALTH_DATA_TYPES:
		return HttpResponseBadRequest('Invalid datattype')
	hds = HealthData.objects.filter(dataTypeName=dataType).filter(startTime_gte=startTime).filter(endTime_lte=endTime)
	if dataType in ['com.google.weight', 'com.google.height']:
		hd = hds.last()
		if hd is None:
			return HttpResponse()
		else:
			return HttpResponse(json.dumps({'value':hd.intVal}))
	val = hds.annotate(Sum('intVal'))
	return HttpResponse(json.dumps({'value':val}))

def getAllData(request):
	if request.method != 'GET':
		return HttpResponseBadRequest('Invalid request method. Must be GET')
	dataType = request.GET.get('datatype')
	startTime = request.GET.get('starttime')
	endTime = request.GET.get('endTime')
	if dataType is None or startTime is None or endTime is None:
		return HttpResponseBadRequest('Invalid parameters. must contain datatype, starttime, endtime')
	if dataType not in AVAILABLE_HEALTH_DATA_TYPES:
		return HttpResponseBadRequest('Invalid datattype')
	hds = HealthData.objects.filter(dataTypeName=dataType).filter(startTime_gte=startTime).filter(endTime_lte=endTime)
	res = []
	if hds is None:
		return HttpResponse()
	for hd in hds:
		res.append(HealthDataSerializer(hd).data)
	return HttpResponse(json.dumps(res))