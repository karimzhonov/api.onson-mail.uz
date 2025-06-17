from django.db import models


class Food(models.Model):
    code = models.SlugField(primary_key=True)
    name = models.CharField('Название', max_length=255)
    description = models.TextField("Описание", max_length=3000, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Питание'
        verbose_name_plural = 'Питании'


class Type(models.Model):
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание", max_length=3000, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'


class Service(models.Model):
    name = models.CharField("Название", max_length=255)
    description = models.TextField("Описание", max_length=3000, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
