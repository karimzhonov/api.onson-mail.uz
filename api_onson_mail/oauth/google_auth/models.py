from django.db import models
from django.db.transaction import atomic
from django.contrib.auth import get_user_model


class GoogleUser(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    email = models.EmailField()
    verified_email = models.BooleanField(default=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    given_name = models.CharField(max_length=255, blank=True, null=True)
    access_token = models.TextField()
    user = models.OneToOneField("oauth.User", models.CASCADE)

    def __str__(self):
        return str(self.email)
    

    @classmethod
    def update_or_create(cls, data):
        from .serializers import GoogleUserSerializer
        with atomic():
            instance = cls.objects.filter(id=data['id']).first()
            if instance:
                serializer = GoogleUserSerializer(instance, data, partial=True)
            else:
                UserModel = get_user_model()
                user = UserModel.objects.create(
                    first_name=data.get('name'),
                )
                data['user'] = user.id
                serializer = GoogleUserSerializer(data=data)
            serializer.is_valid(True)
            serializer.save()
            return serializer.instance

