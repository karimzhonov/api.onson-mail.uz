from rest_framework.generics import CreateAPIView
from .serializers import GoogleUserTokenSerializer


class GoogleAuthView(CreateAPIView):
    serializer_class = GoogleUserTokenSerializer
    permission_classes = ()
    authentication_classes = ()
