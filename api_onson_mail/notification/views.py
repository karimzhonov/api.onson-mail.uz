from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from .serializers import SaveWebPushInformationSerializer
from webpush.models import PushInformation


class SaveWebPushInformationView(CreateAPIView):
    serializer_class = SaveWebPushInformationSerializer

    def create(self, request, *args, **kwargs):
        request.data.update(user=self.request.user.id)
        instance = PushInformation.objects.filter(subscription__endpoint=request.data.get('endpoint')).first()
        if instance:
            serializer = self.get_serializer(instance, request.data, partial = True)
            serializer.is_valid(True)
            serializer.save()
            return Response(serializer.data)
        return super().create(request, *args, **kwargs)