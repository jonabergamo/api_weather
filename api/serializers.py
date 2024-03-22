from rest_framework import serializers
from .models import WeatherEntity

class WeatherSerializer(serializers.Serializer):
    temperature = serializers.FloatField()
    date = serializers.DateTimeField(format="%d/%m/%Y %H:%M:%S")
    city = serializers.CharField(max_length=255, allow_blank=True)
    atmospheric_pressure = serializers.FloatField()
    humidity =  serializers.FloatField()
    weather = serializers.CharField(max_length=255, allow_blank=True)
    
    
    def create(self, validated_data):
        return WeatherEntity(**validated_data)
