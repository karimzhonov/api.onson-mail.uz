from django.db import models
from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from modeltranslation.admin import TabbedTranslationAdmin
from .models import (
    Region, Tour, Type, Country, Food, Service
)
from .inlnes import (
    DayInline, ImageInline, PriceInline
)


@admin.register(Service)
class ServiceAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ['name_uz', 'name_ru']


@admin.register(Food)
class FoodAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ['name_uz', 'name_ru']


@admin.register(Country)
class CountryAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ['name_uz', 'name_ru']


@admin.register(Region)
class RegionAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ['name_uz', 'name_ru', 'country']


@admin.register(Type)
class TypeAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ['name_uz', 'name_ru']


@admin.register(Tour)
class TourAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ['from_country', 'to_country', 'title_ru', 'from_date', 'to_date']
    list_display_links = ["from_country", "to_country", 'title_ru']
    list_filter = ['type']
    inlines = [ImageInline, DayInline, PriceInline]
    filter_horizontal = ['type', 'services']

    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        }
    }
