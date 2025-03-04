from django.db import models

TYPES = (
    ('iftor', 'Iftor'),
    ('saxar', 'Saxar'),
    ('hayit', 'Hayit'),
)

class Day(models.Model):
    date_time = models.DateField(blank=True, null=True)
    name_uz = models.CharField(max_length=255)
    name_ru = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=TYPES)

    def __str__(self):
        return self.name_uz
