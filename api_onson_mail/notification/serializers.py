from django.db.transaction import atomic
from rest_framework import serializers
from webpush.models import SubscriptionInfo, PushInformation


class SubscriptionInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionInfo
        fields = "__all__"


class SaveWebPushInformationSerializer(serializers.ModelSerializer):
    subscription = SubscriptionInfoSerializer()

    class Meta:
        model = PushInformation
        fields = ['user', 'subscription']

    @atomic
    def create(self, validated_data):
        instance = PushInformation.objects.filter(subscription__endpoint=validated_data['subscription']['endpoint']).first()
        if instance:
            return instance
        serializer = SubscriptionInfoSerializer(data=validated_data['subscription'])
        serializer.is_valid(True)
        serializer.save()
        validated_data['subscription'] = serializer.instance
        return super().create(validated_data)
