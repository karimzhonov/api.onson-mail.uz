from unfold.admin import StackedInline, TabularInline
from modeltranslation.admin import TranslationStackedInline
from .models import HotelFood, HotelRoom, HotelService, HotelImage


class HotelImageInline(TabularInline):
    model = HotelImage
    tab = True
    extra = 0
    ordering_field = 'ordering'
    hide_ordering_field = True


class HotelFoodInline(TabularInline):
    model = HotelFood
    tab = True
    extra = 0


class HotelRoomInline(TabularInline, TranslationStackedInline):
    model = HotelRoom
    tab = True
    extra = 0


class HotelServiceInline(TabularInline):
    model = HotelService
    tab = True
    extra = 0
