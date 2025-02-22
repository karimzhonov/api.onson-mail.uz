import random, string
import json
from celery import states
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework.settings import api_settings
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django_celery_results.models import TaskResult
from django.utils import timezone

from .filters import TaskResultFilter
from .token import HS512TestAuthentication


class MQTestView(GenericAPIView):
    authentication_classes = (HS512TestAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        print("request.data", request.data)
        return Response(status=200)


class MQTestReceiveView(GenericAPIView):
    authentication_classes = (HS512TestAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print("request.data", request.data)
        return Response({'calculatedId': ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))}, status=200)


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
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return TaskResult.objects.filter(
            task_name='cargo.order.models._send_api_customs_data',
            status=states.SUCCESS, task_kwargs__contains=self.kwargs.get('sub')
        )

    def get_instance(self ,request, *args, **kwargs):
        pk = request.query_params.get('correlationId')
        instance: TaskResult = get_object_or_404(self.get_queryset(), task_id=pk)
        data = json.loads(instance.result).get('data')
        now = timezone.now()
        return Response({
            "responseTime": now.strftime(api_settings.DATETIME_FORMAT),
            "correlationId": pk,
            "data": data
        })

    def get_ids(self, request, *args, **kwargs):
        now = timezone.now()
        queryset = self.filter_queryset(self.get_queryset())
        ids = queryset.values_list("task_id", flat=True)
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
