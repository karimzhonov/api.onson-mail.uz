from django.db import models


class CargoUser(models.Model):
    user = models.OneToOneField("oauth.User", on_delete=models.CASCADE)
    clients = models.ManyToManyField("client.Client")

    @property
    def username(self):
        return f"u{self.user.phone.national_number}"

    