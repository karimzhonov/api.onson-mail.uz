from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Country, Company


@admin.register(Country)
class CountryAdmin(ModelAdmin):
    list_display = ('name', 'code')


@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    list_display = ['name', 'stir']
