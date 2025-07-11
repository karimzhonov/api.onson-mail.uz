from unfold.admin import StackedInline
from .models import HotelFood, HotelRoom, HotelService


class HotelFoodInline(StackedInline):
    model = HotelFood
    tab = True
    extra = 0


class HotelRoomInline(StackedInline):
    model = HotelRoom
    tab = True
    extra = 0


class HotelServiceInline(StackedInline):
    model = HotelService
    tab = True
    extra = 0
