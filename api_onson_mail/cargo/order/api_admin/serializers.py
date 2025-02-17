from rest_framework import serializers

from cargo.client.serializers import ClientSerializer
from cargo.order.models import Order, Part, Country


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    client = ClientSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = [
            "departure_datetime",
            "enter_uzb_datetime",
            "process_customs_datetime",
            "process_local_datetime",
            "process_received_datetime",
        ]


class CountrySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Country
        fields = ['name', 'code']


class PartSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = Part
        fields = '__all__'



class PartCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Part
        fields = "__all__"
