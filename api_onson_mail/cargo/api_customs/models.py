from django.db import models


class System(models.Model):
    company_name = models.CharField(max_length=255)
    system_name = models.CharField(max_length=255, primary_key=True)
    description = models.TextField()
    status = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.company_name