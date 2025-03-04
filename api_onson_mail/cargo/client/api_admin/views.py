from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet

from cargo.client.models import Client
from .serializers import ClientSerializer


class ClientViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'head']
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    search_fields = ['passport', 'pnfl', 'fio']
    pagination_class = LimitOffsetPagination

    def check_object_permissions(self, request, obj: Client):
        if obj.created_user_id == request.user.id:
            raise PermissionDenied("You can't do that")
        return super(ClientViewSet, self).check_object_permissions(request, obj)

    def create(self, request, *args, **kwargs):
        request.data['created_user'] = request.user.pk
        return super(ClientViewSet, self).create(request, *args, **kwargs)