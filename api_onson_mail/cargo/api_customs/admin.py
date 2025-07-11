from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import System

@admin.register(System)
class SystemAdmin(ModelAdmin):
    list_display = ['company_name', 'company']
    list_editable = ['company']
    
