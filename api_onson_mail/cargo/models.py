from django.db import models


class User(models.Model):
    user = models.OneToOneField("oauth.User", on_delete=models.CASCADE)
    clients = models.ManyToManyField("client.Client")
