from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from .serializers import OptSerializer, OptVerifySerializer, SignUpSerializer, UserShortSerializer

class OptView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = OptSerializer


class OptVerifyView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = OptVerifySerializer


class SignUpView(UpdateAPIView):
    http_method_names = ('patch',)
    serializer_class = SignUpSerializer

    def get_object(self):
        return self.request.user


class MeView(RetrieveAPIView):
    serializer_class = UserShortSerializer

    def get_object(self):
        return self.request.user
