from django.db import models
from django.contrib import admin
from unfold.admin import ModelAdmin, StackedInline
from unfold.contrib.forms.widgets import WysiwygWidget
from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline
from .models import (
    Region, Tour, Type, Price, Day, Country, Food, Hotel, HotelType, Image, Service
)


@admin.register(Service)
class ServiceAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ['name_uz', 'name_ru']


@admin.register(Hotel)
class HotelAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ['name_uz', 'name_ru']


@admin.register(HotelType)
class HotelTypeAdmin(TabbedTranslationAdmin, ModelAdmin):
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


class DayInline(TranslationStackedInline, StackedInline):
    model = Day
    ordering_field = 'day'
    tab = True
    extra = 0


class PriceInline(TranslationStackedInline, StackedInline):
    model = Price
    tab = True
    extra = 0


class ImageInline(StackedInline):
    model = Image
    tab = True
    ordering_field = 'ordering'
    hide_ordering_field = True
    extra = 0


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
