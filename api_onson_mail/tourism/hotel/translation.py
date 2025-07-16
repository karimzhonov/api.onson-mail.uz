from modeltranslation import translator

from .models import HotelType, HotelRoomType, HotelServiceType, Hotel, HotelRoom


@translator.register(HotelType)
class HotelTypeTranslationOptions(translator.TranslationOptions):
    fields = ('name', 'description')


@translator.register(HotelRoomType)
class HotelRoomTypeTranslationOptions(translator.TranslationOptions):
    fields = ('name', 'description')


@translator.register(HotelRoom)
class HotelRoomTranslationOptions(translator.TranslationOptions):
    fields = ('description',)


@translator.register(HotelServiceType)
class HotelServiceTypeTranslationOptions(translator.TranslationOptions):
    fields = ('name', 'description')


@translator.register(Hotel)
class HotelTranslationOptions(translator.TranslationOptions):
    fields = ('name', 'description')
