from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'user']
