from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import ClientSerializer


class ClientViewSet(ReadOnlyModelViewSet):
    serializer_class = ClientSerializer

    def get_queryset(self):
        return self.request.user.cargo.clients.all()
