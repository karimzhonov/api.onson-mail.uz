from rest_framework import serializers
from cargo.client.serializers import ClientSerializer
from oauth.serializers import UserShortSerializer
from .models import CargoUser


class MeSerializer(serializers.ModelSerializer):
    user = UserShortSerializer()
    clients = ClientSerializer(many=True)

    class Meta:
        model = CargoUser
        fields = ["user", "clients"]