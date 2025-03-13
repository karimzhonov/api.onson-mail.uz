from rest_framework.generics import RetrieveAPIView

from .models import CargoUser
from .serializers import MeSerializer


class MeView(RetrieveAPIView):
    serializer_class = MeSerializer

    def get_object(self):
        user, _ = CargoUser.objects.get_or_create(user=self.request.user)
        return user
