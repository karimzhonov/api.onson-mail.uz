from rest_framework import serializers

from .models import Country, Company


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        exclude = ('public_key', 'private_key')


class CountrySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Country
        fields = ['name', 'code']