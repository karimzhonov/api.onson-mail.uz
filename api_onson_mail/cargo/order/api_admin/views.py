from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from contrib.renderers import XLSXRenderer

from ..models import Order, Part, Product
from . import serializers
from .xlsxs import generate_invoice
from .filters import OrderFilter, PartFilter


class OrderViewSet(ModelViewSet):
    perms = ['order.order']
    serializer_class = serializers.OrderSerializer
    filterset_class = OrderFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.OrderSerializer
        return serializers.OrderCreateSerializer

    def get_renderers(self):
        if self.action == 'xlsx':
            return [XLSXRenderer()]
        return super(OrderViewSet, self).get_renderers()

    def get_queryset(self):
        return Order.objects.filter(parts__country__company__in=self.request.user.companies.all()).order_by("-create_time")

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
            order.send_api_customs_data()
        serializer = serializers.OrderSerializer(order, context=self.get_serializer_context())
        return Response(serializer.data)


class PartViewSet(ModelViewSet):
    perms = ['order.part']
    serializer_class = serializers.PartSerializer
    filterset_class = PartFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.PartSerializer
        return serializers.PartCreateSerializer

    def get_queryset(self):
        return Part.objects.filter(country__company__in=self.request.user.companies.all()).order_by("-date")


class ProductViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'head']
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.all()
    search_fields = ['name']
