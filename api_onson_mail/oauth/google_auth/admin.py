from django.contrib import admin
from .models import GoogleUser


@admin.register(GoogleUser)
class GoogleUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'name', 'user']
