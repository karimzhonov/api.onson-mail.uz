from django.contrib import admin
from unfold.admin import ModelAdmin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import HotelType, HotelRoomType, HotelServiceType, Hotel
from .inlines import HotelFoodInline, HotelRoomInline, HotelServiceInline


@admin.register(HotelType)
class HotelTypeAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ['name_uz', 'name_ru']


@admin.register(HotelServiceType)
class HotelServiceTypeAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ['name_uz', 'name_ru']


@admin.register(HotelRoomType)
class HotelRoomTypeAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ['name_uz', 'name_ru']


@admin.register(Hotel)
class HotelAdmin(TabbedTranslationAdmin, ModelAdmin):
    list_display = ['name_uz', 'name_ru']
    inlines = [HotelFoodInline, HotelRoomInline, HotelServiceInline]