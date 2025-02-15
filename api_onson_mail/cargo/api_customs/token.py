import jwt
from datetime import timedelta
from django.conf import settings
from rest_framework_simplejwt.utils import aware_utcnow, datetime_to_epoch

try:
    private_key = open(settings.BASE_DIR / 'private_key.rsa', 'rb').read()
    public_key = open(settings.BASE_DIR / 'public_key.rsa', 'rb').read()
except FileNotFoundError:
    private_key = None
    public_key = None


def get_token():
    current_time = aware_utcnow()
    payload = {
        'sub': '"ONSONMAILCARGO" MCHJ',
        'exp': datetime_to_epoch(current_time + timedelta(days=3)),
        'iat': datetime_to_epoch(current_time)
    }
    return jwt.encode(payload, private_key, algorithm='RS512')


def decode_token(token):
    return jwt.decode(token, public_key, algorithms=['RS512'])
