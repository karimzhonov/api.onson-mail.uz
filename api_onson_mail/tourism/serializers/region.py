from rest_framework import serializers

from ..models import Country, Region


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class RegionSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    class Meta:
        model = Region
        fields = "__all__"