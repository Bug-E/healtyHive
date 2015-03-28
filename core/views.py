from django.http import HttpResponse, HttpResponseBadRequest
import json
from django.shortcuts import get_object_or_404
from core.models import HealthyBee, HealthyBeeAuth, HealthData, BeeCoupons,\
	HealthCoupon
from googleauth.views import getRequestUrl
from django.db.models import Sum
import time
from datetime import datetime, date
from core.serializers import HealthyBeeSerializer

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

def listUsers(request):
	hbs = HealthyBee.objects.all()
	res = []
	for hb in hbs:
		res.append(HealthyBeeSerializer(hb).data)
	return HttpResponse(json.dumps(res))

def getAuthorizationUrl(request):
	if request.method != 'GET':
		return HttpResponseBadRequest('Invalid Method')
	if request.GET.get('bee_id') is None:
		return HttpResponseBadRequest('missing param: bee_id')
	url = getRequestUrl(request.GET['bee_id'])
	return HttpResponse(json.dumps({'url':url}))

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
	bee_id = request.GET.get('bee_id')
	dataType = request.GET.get('datatype')
	startTime = request.GET.get('starttime')
	endTime = request.GET.get('endtime')
	if dataType is None or startTime is None or endTime is None or bee_id is None:
		return HttpResponseBadRequest('Invalid parameters. must contain datatype, starttime, endtime, bee_id')
	startTime = int(startTime)
	endTime = int(endTime)
	if dataType not in AVAILABLE_HEALTH_DATA_TYPES:
		return HttpResponseBadRequest('Invalid datattype')
	val = getDataForUser(bee_id, dataType, startTime, endTime)
	return HttpResponse(json.dumps({'value':val}))

def userdata(request):
	hb = get_object_or_404(HealthyBee, pk=request.GET['bee_id'])
	return HttpResponse(json.dumps(getDataMatrixForUser(hb.pk)))

def leaderboard(request):
	res = []
	hbs = HealthyBee.objects.all()
	for hb in hbs:
		hba = HealthyBeeAuth.objects.filter(bee=hb).first()
		data = getDataMatrixForUser(hb.pk)	
		if hba is None:
			request_url = getRequestUrl(hb.pk)
			data['url'] = request_url
		res.append(data)
	return HttpResponse(json.dumps(res))

def getDataForUser(bee_id, dataType, startTime, endTime):
	bee = get_object_or_404(HealthyBee, pk=bee_id)
	hds = HealthData.objects.filter(dataTypeName=dataType, bee=bee).filter(startTime__gte=startTime).filter(endTime__lte=endTime)
	if dataType in ['com.google.weight', 'com.google.height']:
		hd = hds.last()
		if hd is None:
			return None
		else:
			return hd.intVal
	val = hds.aggregate(val=Sum('intVal'))['val']
	val = 0 if val is None else val
	return val


def getDataMatrixForUser(bee_id):
	hb = HealthyBee.objects.get(pk=bee_id)
	current_timestamp = int(time.time())
	month_before_timestamp = current_timestamp - 30*24*60*60
	weight = getDataForUser(bee_id, 'com.google.weight', month_before_timestamp, current_timestamp)
	height = getDataForUser(bee_id, 'com.google.height', month_before_timestamp, current_timestamp)
	beeCoupons = BeeCoupons.objects.filter(bee=hb)
	_beeCoupons = []
	for beeCoupons in beeCoupons:
		_beeCoupons.append([beeCoupons.coupon.pk, beeCoupons.coupon.name])
	user_data = {
				'pk':hb.pk,
				'name':hb.name,
				'email':hb.email,
				'weight':weight,
				'height':height,
				'coupons':_beeCoupons,
# 				'score':
				}
	dailyCourse = []
	stepData = []
	today = date.today()
	startOfDay = int(today.strftime("%s"))
	distance = getDataForUser(bee_id, 'com.google.distance.delta', startOfDay, current_timestamp)
	steps = getDataForUser(bee_id, 'com.google.step_count.delta', startOfDay, current_timestamp)
	dailyCourse.append([steps, distance])
	stepData.append(steps)
	stepsThisWeek = getDataForUser(bee_id, 'com.google.step_count.delta', startOfDay - 6*24*60*60, current_timestamp)
	user_data['steps_this_week'] = stepsThisWeek
	for day in range(1, 7):
		#pass
		endTime = startOfDay - (day-1)*24*60*60
		startTime = (startOfDay - day*24*60*60)
		distance = getDataForUser(bee_id, 'com.google.distance.delta', startTime, endTime)
		steps = getDataForUser(bee_id, 'com.google.step_count.delta', startTime, endTime)
		dailyCourse.append([steps, distance])
		stepData.append(steps)
	user_data['score'] = dailyCourse[0][0]*100/5000
	user_data['dailyCourse'] = dailyCourse
	stepData.reverse()
	user_data['stepData'] = stepData
	return user_data

def addBeeCoupon(request):
	bee = get_object_or_404(HealthyBee, pk=request.POST['bee_id'])
	coupon = get_object_or_404(HealthCoupon, pk=request.POST['coupon_id'])
	hbc = BeeCoupons()
	hbc.bee = bee
	hbc.coupon = coupon
	hbc.save()
	return HttpResponse()

def addCoupon(request):
	name = request.POST['name']
	coupon = HealthCoupon(name=name)
	coupon.save()
	return HttpResponse()

def listCoupons(request):
	couponList = []
	coupons = HealthCoupon.objects.all()
	for coupon in coupons:
		couponList.append([coupon.pk, coupon.name])
	return HttpResponse(json.dumps(couponList))

	