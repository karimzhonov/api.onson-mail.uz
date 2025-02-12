from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from contrib.renderers import PDFRenderer
from . import serializers
from ..models import Order, Part
from .pdf import generate_invoices


class OrderViewSet(ModelViewSet):
    perms = ['order.order']
    serializer_class = serializers.OrderSerializer

    def get_renderers(self):
        if self.action == 'pdf':
            return [PDFRenderer()]
        return super(OrderViewSet, self).get_renderers()

    def get_queryset(self):
        return Order.objects.filter(parts__country__in=self.request.user.countries.all())

    @action(detail=True, methods=['get'])
    def pdf(self, request, pk=None):
        order = self.get_object()
        data = generate_invoices([order])
        headers = {
            'Content-Disposition': f'filename="Invoice_{order.number}.pdf"',
            'Content-Length': len(data),
        }
        return Response(data, headers=headers, status=200)


class PartViewSet(ModelViewSet):
    perms = ['order.part']
    serializer_class = serializers.PartSerializer

    def get_queryset(self):
        return Part.objects.filter(country__in=self.request.user.countries.all())
