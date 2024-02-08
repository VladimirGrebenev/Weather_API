from rest_framework import serializers
from weather.models import City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class WeatherSerializer(serializers.Serializer):
    city = serializers.CharField()

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        instance['city'] = validated_data.get('city', instance['city'])
        return instance
