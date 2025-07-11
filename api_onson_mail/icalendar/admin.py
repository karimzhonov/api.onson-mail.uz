from django.contrib import admin
from import_export.admin import ImportExportMixin
from unfold.admin import ModelAdmin
from .models import Day


@admin.register(Day)
class CalendarAdmin(ImportExportMixin, ModelAdmin):
    list_display = ['name_ru', 'name_uz']
