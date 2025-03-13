from rest_framework.viewsets import ReadOnlyModelViewSet
from .serializers import ClientSerializer
from .models import Client

class ClientViewSet(ReadOnlyModelViewSet):
    serializer_class = ClientSerializer

    def get_queryset(self):
        return self.request.user.cargouser.clients.all() if hasattr(self.request.user, 'cargouser') else Client.objects.none()
