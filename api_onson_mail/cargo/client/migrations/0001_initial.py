# Generated by Django 4.1.5 on 2025-02-07 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pnfl', models.CharField(max_length=255, unique=True, verbose_name='ПИНФЛ')),
                ('passport', models.CharField(max_length=255, unique=True, verbose_name='Паспорт серия и номер')),
                ('fio', models.CharField(max_length=255, verbose_name='ФИО')),
                ('create_date', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Паспорт клиента',
                'verbose_name_plural': 'Паспорта клиентов',
            },
        ),
    ]
