# Generated by Django 4.1.5 on 2025-03-22 01:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cargo', '0003_rename_user_cargouser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargouser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
