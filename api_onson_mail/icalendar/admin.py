from django.contrib import admin
from import_export.admin import ImportExportMixin
from .models import Day


@admin.register(Day)
class CalendarAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['name_ru', 'name_uz']
