from unfold.admin import StackedInline
from modeltranslation.admin import TranslationStackedInline
from .models import Day, Price, Image


class DayInline(TranslationStackedInline, StackedInline):
    model = Day
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
