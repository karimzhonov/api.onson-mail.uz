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

    def create(self, request, *args, **kwargs):
        pnfl = request.data.get("pnfl")
        request.data.update(created_user=self.request.user)
        client = Client.objects.filter(pnfl=pnfl).first()
        if client:
            serializer = ClientSerializer(client, request.data, partial=True)
        else:
            serializer = ClientSerializer(data=request.data)
        serializer.is_valid(True)
        serializer.save()
        cargouser, _ = CargoUser.objects.get_or_create(user=request.user)
        if not cargouser.clients.filter(id=serializer.instance.id).exists():
            cargouser.clients.add(serializer.instance)
        return Response({}, 200)
