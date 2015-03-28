from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from core.models import HealthyBee, HealthyBeeAuth

# Create your views here.


client_id = '961055264477-pfb2ntjs4fvd3b7vs0ljjbgujjdcfbkc.apps.googleusercontent.com'
email_address = '961055264477-pfb2ntjs4fvd3b7vs0ljjbgujjdcfbkc@developer.gserviceaccount.com'
scope = 'https://www.googleapis.com/auth/fitness.activity.read https://www.googleapis.com/auth/fitness.body.read https://www.googleapis.com/auth/fitness.location.read'
redirect_uri = 'http://stag-sentry-sourabh-sesmic.practodev.com/googleauth/googlecallback'
client_secret = 'JvvjPNBE-IBIjmhJDVduAxHV'

def getRequestUrl(bee_id):
    url = 'https://accounts.google.com/o/oauth2/auth?scope=' + scope +   '&redirect_uri=' + redirect_uri + '&response_type=code&client_id=' +    client_id +    '&approval_prompt=force&include_granted_scopes=true&access_type=offline'
    bee = get_object_or_404(HealthyBee, pk=bee_id)
    url = url + '&state=' + bee.email
    return url

def getResponse(request):
    email = request.GET['state']
    code = request.GET['code']
    data={'code':code,
            'client_id':client_id,
            'client_secret':client_secret,
            'redirect_uri':redirect_uri,
            'grant_type':'authorization_code',
            'access_type':'offline'}
    url = 'https://www.googleapis.com/oauth2/v3/token'
    import requests, json
    r = requests.post(url, data=data)
    access_token = json.loads(r.content)['access_token']
    refresh_token = json.loads(r.content)['refresh_token']
    bee = get_object_or_404(HealthyBee, email=email)
    hba = HealthyBeeAuth.objects.filter(bee=bee)
    if not hba:
        hba = HealthyBeeAuth(bee=bee, token=access_token, refresh_token=refresh_token)
    else:
        hba = hba[0]
        hba.token = access_token
        hba.refresh_token = refresh_token
    hba.save()
    from update_data import updateDataForBee
    updateDataForBee(hba.bee.pk)
    return HttpResponse('Yay! Now you can see your health report and compete in the HealthyHive.')
