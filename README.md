# healtyHive

## Add Bee
```
POST http://stag-sentry-sourabh-sesmic.practodev.com/core/addbee

name=Aditya&email=aditya.subramanyam@practo.com
```

###Response###
```
{"pk": 2, "name": "Aditya", "email": "aditya.subramanyam@practo.com"}
```

## Check if authorized

```
GET http://stag-sentry-sourabh-sesmic.practodev.com/core/isauthorized?bee_id=2
```

### Response ###
```
{"authorized": false}
```

## Get authorization url
```
GET http://stag-sentry-sourabh-sesmic.practodev.com/core/authorizationurl?bee_id=2
```

### Response ###
```
{"url": "https://accounts.google.com/o/oauth2/auth?scope=https://www.googleapis.com/auth/fitness.activity.read https://www.googleapis.com/auth/fitness.body.read https://www.googleapis.com/auth/fitness.location.read&redirect_uri=http://stag-sentry-sourabh-sesmic.practodev.com/googleauth/googlecallback&response_type=code&client_id=961055264477-pfb2ntjs4fvd3b7vs0ljjbgujjdcfbkc.apps.googleusercontent.com&approval_prompt=force&include_granted_scopes=true&access_type=offline&state=aditya.subramanyam@practo.com"}
```

## DATA APIs

### data types 
- 'com.google.weight'
- 'com.google.height'
- 'com.google.step_count.delta'
- 'com.google.distance.delta'

### Request ###
```
GET http://stag-sentry-sourabh-sesmic.practodev.com/core/aggregatehealthdata?bee_id=1&datatype=com.google.weight&starttime=1427402601&endtime=1427512601
```

### Response ###
```
{"value": 70}
```

### Request ###
```
GET http://stag-sentry-sourabh-sesmic.practodev.com/core/aggregatehealthdata?bee_id=1&datatype=com.google.height&starttime=1427402601&endtime=1427512601
```

### Response ###
```
{"value": 175}
```


### Request ###
```
http://stag-sentry-sourabh-sesmic.practodev.com/core/aggregatehealthdata?bee_id=1&datatype=com.google.distance.delta&starttime=1427402601&endtime=1427512601```

### Response ###
```
{"value": 63}
```


### Request ###
```
http://stag-sentry-sourabh-sesmic.practodev.com/core/aggregatehealthdata?bee_id=1&datatype=com.google.step_count.delta&starttime=1427402601&endtime=1427512601
### Response ###
```
{"value": 2876}
```


