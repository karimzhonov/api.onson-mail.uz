from rest_framework import serializers
from ..client.serializers import ClientSerializer
from .models import Order, ProductInOrder, Product


class OrderSerializer(serializers.ModelSerializer):
    fio = serializers.SerializerMethodField()
    status = serializers.CharField()
    client = ClientSerializer()

    class Meta:
        model = Order
        fields = [
            'id', 'number', 'fio', 'weight', 'create_time', 'client',
            'delivery_price', 'departure_datetime', 'enter_uzb_datetime', 'process_customs_datetime',
            'process_local_datetime', 'process_received_datetime', 'status'
        ]

    @staticmethod
    def get_fio(obj: Order):
        return str(obj.client.fio)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class ProductInOrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    total_price = serializers.FloatField()

    class Meta:
        model = ProductInOrder
        fields = "__all__"


class OrderByNumberSerializer(OrderSerializer):
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'number', 'fio', 'weight', 'create_time', 'client', 'products',
            'delivery_price', 'departure_datetime', 'enter_uzb_datetime', 'process_customs_datetime',
            'process_local_datetime', 'process_received_datetime', 'status'
        ]

    def get_products(self, obj: Order):
        qs = obj.productinorder_set.all()
        return ProductInOrderSerializer(qs, many=True, context=self.context).data