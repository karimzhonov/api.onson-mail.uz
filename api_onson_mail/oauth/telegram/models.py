from django.db import models
from django.db.transaction import atomic
from django.contrib.auth import get_user_model


class TelegramUser(models.Model):
    id = models.BigIntegerField(primary_key=True)
    auth_date = models.BigIntegerField(blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    hash = models.TextField()
    username = models.SlugField(blank=True, null=True)
    user = models.OneToOneField("oauth.User", models.CASCADE)

    def __str__(self):
        return str(self.username or self.id)
    

    @classmethod
    def update_or_create(cls, data):
        from .serializers import TelegramUserSerializer
        with atomic():
            instance = cls.objects.filter(id=data['id']).first()
            if instance:
                serializer = TelegramUserSerializer(instance, data, partial=True)
            else:
                UserModel = get_user_model()
                user = UserModel.objects.create(
                    first_name=data.get('first_name'),
                    last_name=data.get('last_name'),
                )
                data['user'] = user.id
                serializer = TelegramUserSerializer(data=data)
            serializer.is_valid(True)
            serializer.save()
            return serializer.instance
