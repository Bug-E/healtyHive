from core.models import HealthyBee, HealthyBeeAuth
from django.http import HttpResponse
import json

CLIENT_ID = '961055264477-pfb2ntjs4fvd3b7vs0ljjbgujjdcfbkc.apps.googleusercontent.com'
CLIENT_SECRET = 'JvvjPNBE-IBIjmhJDVduAxHV'


def getAccessToken(user_id):
    hb = HealthyBee.objects.get(pk=user_id)
    hba = HealthyBeeAuth.objects.filter(bee=hb).first()
    refresh_token = hba.refresh_token
    import requests
    data = { 'refresh_token':refresh_token,
            'client_id': CLIENT_ID,
            'client_secret':CLIENT_SECRET,
            'grant_type':'refresh_token'
            }
    url = 'https://www.googleapis.com/oauth2/v3/token'
    r = requests.post(url, data=data)
    hba.token = json.loads(r.content)['access_token']
    hba.save()
    return hba.token

