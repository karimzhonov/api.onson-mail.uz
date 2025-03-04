from django.db import models

TYPES = (
    ('roza', 'Roza'),
    ('hayit', 'Hayit'),
)

class Day(models.Model):
    date_time = models.DateTimeField(blank=True, null=True)
    end_date_time = models.DateTimeField(blank=True, null=True)
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=TYPES)

    def __str__(self):
        return self.name_uz
