from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    fio = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'number', 'fio', 'weight',
            'delivery_price', 'departure_datetime', 'enter_uzb_datetime', 'process_customs_datetime',
            'process_local_datetime', 'process_received_datetime', 'status'
        ]

    @staticmethod
    def get_fio(obj: Order):
        return str(obj.client.fio)

    @staticmethod
    def get_status(obj: Order):
        return str(obj.parts.status)
