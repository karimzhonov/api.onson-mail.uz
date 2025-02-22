from django.contrib import admin

from .models import System

@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'company']
    list_editable = ['company']
    
