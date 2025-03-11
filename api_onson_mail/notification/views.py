from webpush.models import PushInformation
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from .serializers import SaveWebPushInformationSerializer, NotificationSerializer
from .models import Notification


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
    

class NotificationView(ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['unread'] = self.get_queryset().filter(read=False).count()
        return response
    