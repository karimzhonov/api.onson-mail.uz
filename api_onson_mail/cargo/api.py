import requests
import jwt.api_jws
from datetime import timedelta, datetime
from calendar import timegm
from django.conf import settings
from django.utils.timezone import is_naive, make_aware, utc

URL = "https://pushservice.egov.uz/v3/app/mq"


def make_utc(dt):
    if settings.USE_TZ and is_naive(dt):
        return make_aware(dt, timezone=utc)

    return dt

def aware_utcnow():
    return make_utc(datetime.utcnow())


def datetime_to_epoch(dt):
    return timegm(dt.utctimetuple())


def get_token():
    current_time = aware_utcnow()
    private_key = open(settings.BASE_DIR / 'private_key.rsa', 'rb').read()
    payload = {
        'sub': '"ONSONMAILCARGO" MCHJ',
        'exp': datetime_to_epoch(current_time + timedelta(days=3)),
        'iat': datetime_to_epoch(current_time)
    }
    return jwt.encode(payload, private_key, algorithm='RS512')


def decode_token(token):
    public_key = open(settings.BASE_DIR / 'public_key.rsa', 'rb').read()
    return jwt.decode(token, public_key, algorithms=['RS512'])


def request(pk, data):
    url = URL + "/receive"
    token = get_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
    json={
        'correlationId': str(pk),
        'data': data,
    }
    return requests.post(url, json=json, headers=headers)
