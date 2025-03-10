from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from .models import Order, STATUSES
from .serializers import OrderSerializer


class OrderViewSet(ReadOnlyModelViewSet):
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        return Order.objects.filter(client__in=self.request.user.cargo.clients.all())


class StatusView(RetrieveAPIView):
    permission_classes = ()

    def retrieve(self, request, *args, **kwargs):
        statuses = dict(STATUSES)
        for k, v in statuses.items():
            statuses[k] = {"name": v}
        statuses['create_time']["color"] = 'lime'
        statuses['departure_datetime']["color"] = 'gray'
        statuses['enter_uzb_datetime']["color"] = 'red'
        statuses['process_customs_datetime']["color"] = 'orange'
        statuses['process_local_datetime']["color"] = 'blue'
        statuses['process_received_datetime']["color"] = 'green'
        return Response(statuses)