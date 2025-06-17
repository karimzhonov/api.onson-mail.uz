from modeltranslation import translator
from .models import Region, Type, Tour, Price, Day, Hotel, HotelType, Food, Country, Service


@translator.register(Country)
class CountryTranslationOptions(translator.TranslationOptions):
    fields = ('name', )


@translator.register(Region)
class RegionTranslationOptions(translator.TranslationOptions):
    fields = ('name', )


@translator.register(Service)
class ServiceTranslationOptions(translator.TranslationOptions):
    fields = ('name', 'description')


@translator.register(Type)
class TypeTranslationOptions(translator.TranslationOptions):
    fields = ('name', 'description')


@translator.register(HotelType)
class HotelTypeTranslationOptions(translator.TranslationOptions):
    fields = ('name', 'description')


@translator.register(Hotel)
class HotelTranslationOptions(translator.TranslationOptions):
    fields = ('name', 'description')


@translator.register(Tour)
class TourTranslationOptions(translator.TranslationOptions):
    fields = ('title', 'description')


@translator.register(Food)
class FoodTranslationOptions(translator.TranslationOptions):
    fields = ('name', 'description')


@translator.register(Price)
class PriceTranslationOption(translator.TranslationOptions):
    fields = ('name',)


@translator.register(Day)
class DayTranslationOption(translator.TranslationOptions):
    fields = ('title', 'desc')
