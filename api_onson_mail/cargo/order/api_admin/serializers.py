from rest_framework import serializers

from cargo.client.api_admin.serializers import ClientSerializer
from cargo.order.models import Order, Part, ProductInOrder, Product
from company.serializers import CountrySerializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


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
    products = serializers.ListField(child=serializers.JSONField())

    class Meta:
        model = Order
        fields = ['id', 'parts', 'client', 'weight', 'products']

    def create(self, validated_data):
        products = validated_data.pop('products')
        instance = super(OrderCreateSerializer, self).create(validated_data)
        for product in products:
            ProductInOrder.objects.get_or_create(order=instance, product_id=product['product'], count=product['count'])
        instance.products = products
        return instance

    def update(self, instance, validated_data):
        products = validated_data.pop('products')
        for product in products:
            ProductInOrder.objects.get_or_create(order=instance, product_id=product['product'], count=product['count'])
        instance.products = products
        return super(OrderCreateSerializer, self).update(instance, validated_data)


class PartSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = Part
        fields = '__all__'



class PartCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Part
        fields = "__all__"
