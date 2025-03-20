from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from ..models import CargoUser
from .serializers import ClientSerializer
from .models import Client


class ClientViewSet(ModelViewSet):
    http_method_names = ['head', 'get', 'post']
    serializer_class = ClientSerializer

    def get_queryset(self):
        return self.request.user.cargouser.clients.all() if hasattr(self.request.user, 'cargouser') else Client.objects.none()

    def post(self, request, *args, **kwargs):
        pnfl = request.data.get("pnfl")
        client = get_object_or_404(Client, pnfl=pnfl)
        cargouser, _ = CargoUser.objects.get_or_create(user=request.user)
        cargouser.clients.add(client)
        return Response({}, 200)
