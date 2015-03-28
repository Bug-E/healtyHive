from core.models import HealthyBee, HealthyBeeAuth, HealthData
from googleauth.get_access_token import getAccessToken
from datetime import datetime, date
import calendar
import time
import requests
import json

data_streams = ['raw:com.google.weight:com.google.android.apps.fitness:user_input',
        'raw:com.google.height:com.google.android.apps.fitness:user_input',
        'derived:com.google.step_count.delta:com.google.android.gms:estimated_steps',
        'derived:com.google.distance.delta:com.google.android.gms:pruned_distance'
        ]
dataset_url = 'https://www.googleapis.com/fitness/v1/users/me/dataSources/'
hbs = HealthyBee.objects.all()
for hb in hbs:
    print hb.email
    hba = HealthyBeeAuth.objects.filter(bee=hb).first()
    if hba is None:
        print 'not authorized'
        continue
    access_token = getAccessToken(hb.pk)
    last_sync = hb.lastSyncTime
    if last_sync is None:
        last_sync = int(time.time()) - 24*60*60
    sync_upto = int(time.time())
    last_sync *= 1000000000
    sync_upto *= 1000000000
    print last_sync
    print sync_upto
    dataset = str(last_sync) + '-' + str(sync_upto)
    authorization = 'Bearer ' + access_token
    _headers = {'Authorization':authorization}
    def get_data(_url, _headers):
        r = requests.get(_url, headers=_headers)
        response_json = json.loads(r.content)
        for point in response_json.get('point', []):
            startTime = int(point.get('startTimeNanos'))/1000000000
            endTime = int(point.get('endTimeNanos'))/1000000000
            dataTypeName = point.get('dataTypeName')
            originDataSourceId = point.get('originDataSourceId')
            intval = 0

            for v in point.get('value', []):
                intval += int(v.get('intVal', 0))
                if 'height' in dataTypeName:
                    intval = int(float(v.get('fpVal', 0))*100)
                else:
                    intval += int(float(v.get('fpVal', 0)))
            data = HealthData()
            data.bee = hb
            data.startTime = startTime
            data.endTime = endTime
            data.dataTypeName = dataTypeName
            data.originalDataSourceId = originDataSourceId
            data.intVal = intval
            data.save()
        hb.lastSyncTime = sync_upto/1000000000
        hb.save()
    for stream in data_streams:
        _dataset_url = dataset_url + stream + '/datasets/' + dataset
        get_data(_dataset_url, _headers)

#    url =
