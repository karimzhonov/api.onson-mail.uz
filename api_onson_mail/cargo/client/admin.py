from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Client

@admin.register(Client)
class ClientAdmin(ModelAdmin):
    list_display = ["fio", "pnfl", "passport"]
    search_fields = ["fio", "pnfl", "passport"]
