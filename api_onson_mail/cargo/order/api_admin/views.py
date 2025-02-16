from django.utils import timezone
from rest_framework.generics import RetrieveAPIView
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from contrib.renderers import XLSXRenderer

from ..models import Order, Part
from ..product import generate_cart
from . import serializers
from .xlsxs import generate_invoice



class OrderViewSet(ModelViewSet):
    perms = ['order.order']
    serializer_class = serializers.OrderSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.OrderSerializer
        return serializers.OrderCreateSerializer

    def get_renderers(self):
        if self.action == 'xlsx':
            return [XLSXRenderer()]
        return super(OrderViewSet, self).get_renderers()

    def get_queryset(self):
        return Order.objects.filter(parts__country__in=self.request.user.countries.all())

    @action(detail=True, methods=['get'])
    def xlsx(self, request, pk=None):
        order = self.get_object()
        data = generate_invoice(order)
        headers = {
            'Content-Disposition': f'filename="Invoice_{order.number}.xlsx"',
            'Content-Length': len(data),
        }
        return Response(data, headers=headers, status=200)

    @action(detail=True, methods=['patch'])
    def change_status(self, request, pk=None):
        order = self.get_object()
        status = request.data.get('status')
        if hasattr(order, status):
            setattr(order, status, timezone.now())
            order.save()
            order.send_ws_data(self.request.user.id)
        serializer = self.get_serializer(order)
        return Response(serializer.data)


class PartViewSet(ModelViewSet):
    perms = ['order.part']
    serializer_class = serializers.PartSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.PartSerializer
        return serializers.PartCreateSerializer

    def get_queryset(self):
        return Part.objects.filter(country__in=self.request.user.countries.all())


class ProductGeneratorView(RetrieveAPIView):      
    perms = ['order.order']  
    
    def retrieve(self, request, *args, **kwargs):
        try:
            price = float(self.kwargs.get('price'))
        except ValueError:
            raise ValidationError({'price': "Must be number"})
        
        instance = generate_cart(price)
        return Response(instance)
