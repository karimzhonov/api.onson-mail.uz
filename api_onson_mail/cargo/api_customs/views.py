import json
from celery import states
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework.settings import api_settings
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django_celery_results.models import TaskResult
from django.utils import timezone
from cargo.order.models import Order
from .filters import TaskResultFilter

mqview_schema = extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter('correlationId', str),
            OpenApiParameter('date', str),
            OpenApiParameter('subscriberSystem', str),
        ]
    )
)

@mqview_schema
class MQView(ListAPIView):
    filterset_class = TaskResultFilter
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get_instance(request, *args, **kwargs):
        pk = request.query_params.get('correlationId')
        instance: Order = get_object_or_404(Order.objects.all(), pk=pk)
        now = timezone.now()
        return Response({
            "responseTime": now.strftime(api_settings.DATETIME_FORMAT),
            "correlationId": pk,
            "data": instance.serialized_data
        })

    def get_ids(self, request, *args, **kwargs):
        tasks = TaskResult.objects.filter(
            task_name='cargo.order.models._send_request',
            status=states.SUCCESS
        )
        ids = []
        queryset = self.filter_queryset(tasks).values_list("result", flat=True)
        for result in queryset:
            result_json = json.loads(result)
            for row in result_json:
                if not row.get('id') in ids:
                    ids.append(row.get('id'))
        now = timezone.now()
        return Response({
            "date": request.query_params.get('date', now.date()),
            "responseTime": now.strftime(api_settings.DATETIME_FORMAT),
            "count": len(ids),
            "ids": ids,
        })

    def list(self, request, *args, **kwargs):
        if request.query_params.get('correlationId'):
            return self.get_instance(request, *args, **kwargs)
        return self.get_ids(request, *args, **kwargs)
