from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet

from cargo.client.models import Client
from .serializers import ClientSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    search_fields = ['passport', 'pnfl', 'fio']
    pagination_class = LimitOffsetPagination