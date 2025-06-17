from django.db import models


class HotelType(models.Model):
    name = models.CharField('Название', max_length=255)
    description = models.TextField("Описание", max_length=3000, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тип отеля'
        verbose_name_plural = 'Тип отели'


class Hotel(models.Model):
    name = models.CharField('Название', max_length=255)
    description = models.TextField("Описание", max_length=3000, null=True, blank=True)
    stars = models.IntegerField(choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)))
    type = models.ForeignKey(HotelType, models.CASCADE)
    region = models.ForeignKey("tourism.Region", models.PROTECT, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'