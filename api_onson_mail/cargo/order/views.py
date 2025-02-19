from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from .models import Order, STATUSES
from .serializers import OrderSerializer


class OrderByNumberView(RetrieveAPIView):
    lookup_field = 'number'
    lookup_url_kwarg = 'number'
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = ()
    authentication_classes = ()


class StatusView(RetrieveAPIView):

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