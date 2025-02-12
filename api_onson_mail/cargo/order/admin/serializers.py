from rest_framework import serializers

from cargo.order.models import Order, Part


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class PartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Part
        fields = '__all__'
