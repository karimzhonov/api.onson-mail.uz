from rest_framework import serializers

from ..models import Service, Food, Type

class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = "__all__"


class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = "__all__"


class TypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Type
        fields = "__all__"
