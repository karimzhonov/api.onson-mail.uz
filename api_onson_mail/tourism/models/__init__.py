import calendar
from django.db import models

from .others import Food, Type, Service
from .region import Country, Region


WEEKDAY_CHOICES = [(i, calendar.day_name[i].capitalize()) for i in range(7)]


class Tour(models.Model):
    title=models.CharField("Название", max_length=255)
    description=models.TextField("Описание", max_length=3000, null=True, blank=True)
    from_country = models.ForeignKey(Country, models.PROTECT, null=True, related_name='from_country_tour_set')
    to_country = models.ForeignKey(Country, models.PROTECT, null=True, related_name='to_country_tour_set')
    type = models.ManyToManyField(Type, verbose_name="Тип")
    from_date = models.DateField("Начало")
    to_date = models.DateField("Конец")
    from_day = models.IntegerField("День начало тура", choices=WEEKDAY_CHOICES)
    hot_tour = models.BooleanField(default=False)
    best_proposal = models.BooleanField(default=False)
    food = models.ForeignKey(Food, models.SET_NULL, null=True)
    with_flight = models.BooleanField(default=False, verbose_name='Учитивая международный перелети')
    services = models.ManyToManyField(Service, blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Тур'
        verbose_name_plural = 'Туры'
    
    
class Price(models.Model):
    name = models.CharField("Название", max_length=255)
    tour = models.ForeignKey(Tour, models.CASCADE, verbose_name="Тур")
    price_b2b = models.FloatField(verbose_name="Цена B2B")
    price_b2c = models.FloatField(verbose_name="Цена B2C")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Цена тура'
        verbose_name_plural = 'Цены туров'


class Day(models.Model):
    tour = models.ForeignKey(Tour, models.CASCADE, verbose_name="Тур")
    region = models.ForeignKey(Region, models.PROTECT, verbose_name="Где будеть?")
    day = models.PositiveIntegerField("День")
    title = models.CharField("Название", max_length=255, null=True)
    desc = models.TextField("Описание", max_length=3000, null=True)
    image = models.ImageField("Фото", upload_to='tour/day', null=True)
    hotel = models.ForeignKey("hotel.Hotel", models.PROTECT, null=True)

    class Meta:
        ordering = ['day']
        verbose_name = 'День тура'
        verbose_name_plural = 'Дни тура'

    def __str__(self):
        return f"{self.tour} ({self.region})"


class Image(models.Model):
    ordering = models.PositiveIntegerField(default=0)
    tour = models.ForeignKey(Tour, models.CASCADE, null=True)
    image = models.ImageField('Фото', upload_to='tourism/image')

    class Meta:
        ordering = ['ordering']
