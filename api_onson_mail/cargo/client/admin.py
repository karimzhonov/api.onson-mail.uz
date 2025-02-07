from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ["fio", "pnfl", "passport"]
    search_fields = ["fio", "pnfl", "passport"]
