# Generated by Django 4.1.5 on 2025-02-14 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_country_price_per_order_client_order_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='part',
            name='status',
            field=models.CharField(choices=[('departure_datetime', 'Yolga chiqdi'), ('enter_uzb_datetime', 'UZBga keldi'), ('process_customs_datetime', 'Tamojnada'), ('process_local_datetime', 'Dastavkada'), ('process_received_datetime', 'Yetkasib berildi')], default='departure_datetime', max_length=50, verbose_name='Статус'),
        ),
    ]
