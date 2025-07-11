from django.db import models
from simple_history.models import HistoricalRecords


class HotelType(models.Model):
    name = models.CharField('Название', max_length=255)
    description = models.TextField("Описание", max_length=3000, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тип отеля'
        verbose_name_plural = 'Тип отели'


class HotelRoomType(models.Model):
    name = models.CharField('Название', max_length=255)
    description = models.TextField("Описание", max_length=3000, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тип Комната отеля'
        verbose_name_plural = 'Тип Комната отели'


class HotelServiceType(models.Model):
    name = models.CharField('Название', max_length=255)
    description = models.TextField("Описание", max_length=3000, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тип услуги отеля'
        verbose_name_plural = 'Тип услуги отели'


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


class HotelFood(models.Model):
    hotel = models.ForeignKey(Hotel, models.CASCADE)
    food = models.ForeignKey("tourism.Food", models.PROTECT)
    price = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Питание отеля'
        verbose_name_plural = 'Питание отели'


class HotelRoom(models.Model):
    hotel = models.ForeignKey(Hotel, models.CASCADE)
    room = models.ForeignKey(HotelRoomType, models.PROTECT)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    free_rooms = models.IntegerField(null=True, blank=True)

    history = HistoricalRecords()
    
    class Meta:
        verbose_name = 'Комната отеля'
        verbose_name_plural = 'Комната отели'


class HotelService(models.Model):
    hotel = models.ForeignKey(Hotel, models.CASCADE)
    service = models.ForeignKey(HotelServiceType, models.PROTECT)
    price = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Услуги отеля'
        verbose_name_plural = 'Услуги отели'
    