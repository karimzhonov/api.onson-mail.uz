# Generated by Django 4.1.5 on 2025-02-11 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='System',
            fields=[
                ('company_name', models.CharField(max_length=255)),
                ('system_name', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('status', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
