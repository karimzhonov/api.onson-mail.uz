from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import GoogleUser


@admin.register(GoogleUser)
class GoogleUserAdmin(ModelAdmin):
    list_display = ['id', 'email', 'name', 'user']
