import json
from django.contrib.auth.models import update_last_login
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from .authentication import validate
from .models import TelegramUser
from .serializers import TelegramUserSerializer


class TelegramAuthView(CreateAPIView):
    serializer_class = TelegramUserSerializer
    permission_classes = ()
    authentication_classes = ()
    
    def post(self, request, *args, **kwargs):
        validate(json.loads(json.dumps(request.data)))
        telegram_user = TelegramUser.update_or_create(request.data)
        refresh = RefreshToken.for_user(telegram_user.user)
        data = {}
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, telegram_user.user)
        return Response(data)
