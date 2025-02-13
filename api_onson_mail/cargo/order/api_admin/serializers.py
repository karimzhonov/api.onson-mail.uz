from rest_framework import serializers

from cargo.client.serializers import ClientSerializer
from cargo.order.models import Order, Part


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField()
    client = ClientSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class PartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Part
        fields = '__all__'
