from rest_framework import serializers
from tourism.serializers.others import FoodSerializer
from tourism.serializers.region import RegionSerializer
from .models import HotelType, Hotel, HotelRoomType, HotelServiceType, HotelFood, HotelRoom, HotelService, HotelImage


class HotelTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelType
        fields = "__all__"


class HotelRoomTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelRoomType
        fields = '__all__'


class HotelServiceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelServiceType
        fields = "__all__"


class HotelFoodSerializer(serializers.ModelSerializer):
    food = FoodSerializer()
    
    class Meta:
        model = HotelFood
        exclude = ['hotel']


class HotelRoomSerializer(serializers.ModelSerializer):
    room = HotelRoomTypeSerializer()

    class Meta:
        model = HotelRoom
        exclude = ['hotel']


class HotelServiceSerializer(serializers.ModelSerializer):
    service = HotelServiceTypeSerializer()

    class Meta:
        model = HotelService
        exclude = ['hotel']


class HotelImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = HotelImage
        exclude = ['hotel']


class HotelSerializer(serializers.ModelSerializer):
    type = HotelTypeSerializer()
    region = RegionSerializer()
    hotelfood_set = HotelFoodSerializer(many=True)
    hotelroom_set = HotelRoomSerializer(many=True)
    hotelservice_set = HotelServiceSerializer(many=True)
    hotelimage_set = HotelImageSerializer(many=True)

    class Meta:
        model = Hotel
        fields = "__all__"
