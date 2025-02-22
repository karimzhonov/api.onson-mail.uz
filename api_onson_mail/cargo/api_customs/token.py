import jwt
from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.utils import aware_utcnow, datetime_to_epoch
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken



def get_token(sub, private_key):
    current_time = aware_utcnow()
    payload = {
        'sub': sub,
        'exp': datetime_to_epoch(current_time + timedelta(days=3)),
        'iat': datetime_to_epoch(current_time)
    }
    return jwt.encode(payload, private_key, algorithm='RS512')


def decode_token(token, public_key):
    return jwt.decode(token, public_key, algorithms=['RS512'])


class HS512TestAuthentication(JWTAuthentication):
    try:
        publickey = open(settings.BASE_DIR / 'test_public_key.pem', 'rb').read()
    except FileNotFoundError:
        publickey = None

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None
        print(header)
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        try:
            validated_token = decode_token(raw_token, self.publickey)
            print('validated_token: ', validated_token)
        except Exception as e:
            raise InvalidToken(
            {
                "detail": _("Given token not valid for any token type"),
                "messages": [str(e)],
            }
        )

        return get_user_model().objects.first(), validated_token