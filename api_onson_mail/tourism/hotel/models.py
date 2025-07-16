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
    stars = models.IntegerField('Рейтинг', choices=((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)))
    type = models.ForeignKey(HotelType, models.CASCADE, verbose_name="Тип")
    region = models.ForeignKey("tourism.Region", models.PROTECT, null=True, verbose_name='Город')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Отель'
        verbose_name_plural = 'Отели'


class HotelImage(models.Model):
    ordering = models.PositiveIntegerField(default=0)
    hotel = models.ForeignKey(Hotel, models.CASCADE, null=True)
    image = models.ImageField('Фото', upload_to='tourism/hotel/image')

    class Meta:
        ordering = ['ordering']

    class Meta:
        verbose_name = 'Фото отеля'
        verbose_name_plural = 'Фото отеля'
    
    def __str__(self):
        return str(self.image)


class HotelFood(models.Model):
    hotel = models.ForeignKey(Hotel, models.CASCADE)
    food = models.ForeignKey("tourism.Food", models.PROTECT, verbose_name='Питание')
    price_b2b = models.FloatField(blank=True, null=True, verbose_name='Цена (B2B)')
    price_b2c = models.FloatField(blank=True, null=True, verbose_name='Цена (B2C)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Питание отеля'
        verbose_name_plural = 'Питание отели'

    def __str__(self):
        return str(self.food)


class HotelRoom(models.Model):
    hotel = models.ForeignKey(Hotel, models.CASCADE)
    room = models.ForeignKey(HotelRoomType, models.PROTECT, verbose_name='Комната')
    description = models.TextField(max_length=255, blank=True, null=True, verbose_name='Описание')
    price_b2b = models.FloatField(blank=True, null=True, verbose_name='Цена (B2B)')
    price_b2c = models.FloatField(blank=True, null=True, verbose_name='Цена (B2C)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True, null=True, upload_to='tourism/hotel/room', verbose_name='Фото')
    
    class Meta:
        verbose_name = 'Комната отеля'
        verbose_name_plural = 'Комната отели'

    def __str__(self):
        return str(self.room)


class HotelService(models.Model):
    hotel = models.ForeignKey(Hotel, models.CASCADE)
    service = models.ForeignKey(HotelServiceType, models.PROTECT, verbose_name='Услуга')
    price_b2b = models.FloatField(blank=True, null=True, verbose_name='Цена (B2B)')
    price_b2c = models.FloatField(blank=True, null=True, verbose_name='Цена (B2C)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Услуги отеля'
        verbose_name_plural = 'Услуги отели'

    def __str__(self):
        return str(self.service)
    