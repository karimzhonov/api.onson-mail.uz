import requests
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from .models import GoogleUser


class GoogleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoogleUser
        fields = "__all__"


class GoogleUserTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def create(self, validated_data):
        access_token = validated_data.get('access_token')
        response = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', {"access_token": access_token})
        if not response.ok:
            raise AuthenticationFailed(
                _("Given token not valid for any token type"),
                code='bat_token'
            )
    
        response_data = response.json()
        response_data["access_token"] = access_token
        print(response_data)
        user = GoogleUser.update_or_create(response_data)

        refresh = RefreshToken.for_user(user.user)
        data = {}
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user.user)
        return data            
