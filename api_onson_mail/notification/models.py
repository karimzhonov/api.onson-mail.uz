from django.db import models
from django.contrib.auth import get_user_model


class Notification(models.Model):
    user = models.ForeignKey(get_user_model(), models.CASCADE)
    data = models.JSONField(default=dict)
    read = models.BooleanField(default=False)
