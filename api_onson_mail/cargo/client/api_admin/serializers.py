from rest_framework import serializers

from cargo.client.models import Client


class ClientSerializer(serializers.ModelSerializer):
    phones = serializers.CharField(read_only=True)
    can_change = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = '__all__'

    def get_can_change(self, obj):
        return obj.created_user_id == self.context['request'].user.id