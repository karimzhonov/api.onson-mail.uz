# Generated by Django 4.1.5 on 2025-02-16 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_order_facture_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.JSONField(default=dict),
        ),
    ]
