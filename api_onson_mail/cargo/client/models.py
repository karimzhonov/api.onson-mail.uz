from django.db import models


class Client(models.Model):
    pnfl = models.CharField('ПИНФЛ', max_length=255, unique=True)
    passport = models.CharField('Паспорт серия и номер', max_length=255, unique=True)
    fio = models.CharField('ФИО', max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.fio

    class Meta:
        verbose_name = 'Паспорт клиента'
        verbose_name_plural = 'Паспорта клиентов'
