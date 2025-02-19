from rest_framework import serializers

from cargo.client.api_admin.serializers import ClientSerializer
from cargo.order.models import Order, Part, Country, ProductInOrder


class ProductInOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductInOrder
        fields = ['product', 'count']


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    client = ClientSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    products = ProductInOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = ['parts', 'client', 'weight', 'products']


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
