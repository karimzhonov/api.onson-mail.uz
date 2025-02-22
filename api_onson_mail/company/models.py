from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=255)
    stir = models.CharField(max_length=255)
    sub = models.CharField(max_length=255)
    public_key = models.TextField()
    private_key = models.TextField()

    def __str__(self):
        return self.name
    

class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    send_org = models.CharField(max_length=100, blank=True, null=True)
    price_per = models.FloatField()
    company = models.ForeignKey(Company, models.CASCADE)

    def __str__(self):
        return self.name
