from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken


class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        close_old_connections()
        try:
            jwt_token_list = parse_qs(scope["query_string"].decode("utf8")).get('token', [None])
            jwt_token = jwt_token_list[0]
            try:
                token = AccessToken(jwt_token)
            except TokenError:
                raise InvalidToken()
            scope['user'] = await self.get_user(token)
        except (KeyError, AuthenticationFailed, InvalidToken):
            scope['user'] = AnonymousUser()
        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_user(self, validated_token):
        User = get_user_model()
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(_("Token contained no recognizable user identification"))

        try:
            user = User.objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except User.DoesNotExist:
            raise AuthenticationFailed(_("User not found"), code="user_not_found")

        if not user.is_active:
            raise AuthenticationFailed(_("User is inactive"), code="user_inactive")
        return user


class IsAuthenticatedMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope['user'].is_anonymous or not scope['user'].is_authenticated:
            return None
        return await self.app(scope, receive, send)


def WebsocketMiddlewareStack(app):
    return JWTAuthMiddleware(IsAuthenticatedMiddleware(app))