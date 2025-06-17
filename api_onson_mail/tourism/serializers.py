from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Type, Region, Tour, Day, Price, Image, Country, Hotel, HotelType, Food, Service



class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = "__all__"


class HotelTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelType
        fields = "__all__"


class HotelSerializer(serializers.ModelSerializer):
    type = HotelTypeSerializer()
    region = RegionSerializer()
    
    class Meta:
        model = Hotel
        fields = "__all__"


class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = "__all__"


class TypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Type
        fields = "__all__"




class DaySerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    hotel = HotelSerializer()
    
    class Meta:
        model = Day
        exclude = ['tour']


class PriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Price
        exclude = ['tour']


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        exclude = ['tour']


class TourListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    type = TypeSerializer(many=True)
    min_price_b2b = serializers.FloatField(required=False)
    min_price_b2c = serializers.FloatField(required=False)

    class Meta:
        model = Tour
        fields = ['id', 'images', 'type', 'title', 'title_uz', 'title_ru', 'description', 'description_uz', 'description_ru', 'min_price_b2b', 'min_price_b2c', 'hot_tour', 'best_proposal']

    @extend_schema_field(ImageSerializer(many=True))
    def get_images(self, obj: Tour):
        return ImageSerializer(obj.image_set.all(), many=True, context=self.context).data


class TourSerializer(serializers.ModelSerializer):
    days = serializers.SerializerMethodField()
    prices = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    services = ServiceSerializer(many=True)
    type = TypeSerializer(many=True)
    min_price_b2b = serializers.FloatField(required=False)
    min_price_b2c = serializers.FloatField(required=False)
    food = FoodSerializer()

    class Meta:
        model = Tour
        fields = "__all__"

    @extend_schema_field(DaySerializer(many=True))
    def get_days(self, obj: Tour):
        return DaySerializer(obj.day_set.all(), many=True, context=self.context).data
    
    @extend_schema_field(PriceSerializer(many=True))
    def get_prices(self, obj: Tour):
        return PriceSerializer(obj.price_set.all(), many=True, context=self.context).data

    @extend_schema_field(ImageSerializer(many=True))
    def get_images(self, obj: Tour):
        return ImageSerializer(obj.image_set.all(), many=True, context=self.context).data
