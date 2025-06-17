from django.db import models


class Country(models.Model):
    name=models.CharField('Название', max_length=255)
    can_from = models.BooleanField('Откуда (показать?)', default=True)
    can_to = models.BooleanField('Куда (показать?)', default=True)
    active = models.BooleanField('Актив?', default=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страна'


class Region(models.Model):
    name = models.CharField('Название', max_length=255)
    country = models.ForeignKey(Country, models.CASCADE, null=True)
    can_from = models.BooleanField('Откуда (показать?)', default=True)
    can_to = models.BooleanField('Куда (показать?)', default=True)
    active = models.BooleanField('Актив?', default=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

