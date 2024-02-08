import time

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from weather.models import City
from weather.serializers import CitySerializer, WeatherSerializer
from config.settings import YANDEX_WEATHER_API_KEY
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import redis
from datetime import datetime, timedelta
import json

# Подключение к Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)


class WeatherView(APIView):
    serializer_class = WeatherSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('city', openapi.IN_QUERY,
                              description="City name",
                              type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request):
        serializer = self.serializer_class(data=request.GET)
        serializer.is_valid(raise_exception=True)

        city_name = serializer.validated_data.get('city', '')

        # Проверка кэша
        cache_key = f'weather:{city_name}'
        cached_data = redis_client.get(cache_key)

        if cached_data:
            weather_data = json.loads(cached_data)
            cache_time = datetime.strptime(weather_data['cache_time'],
                                           '%Y-%m-%d %H:%M:%S')
            if datetime.now() - cache_time <= timedelta(minutes=30):
                return Response(weather_data['data'])

        cities = City.objects.filter(name=city_name)

        if not cities:
            return Response({'error': 'Город не найден'}, status=404)

        # это потенциально баг, потому что берётся первый подошедший город
        # из списка, а названия городов бывают одинаковые, нужно конечно ещё
        # запрашивать область/край
        city = cities.first()

        lat = city.lat
        lon = city.lon

        url = f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}&lang=ru_RU"
        headers = {'X-Yandex-API-Key': YANDEX_WEATHER_API_KEY}

        # time.sleep(3) # имитация задержки для проверки работы redis cache

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            weather_data = response.json()
            city_serializer = CitySerializer(city)
            city_data = city_serializer.data
            city_name = city_data['name']
            temp_celsius = weather_data['fact']['temp']
            pressure_mm = weather_data['fact']['pressure_mm']
            wind_speed = weather_data['fact']['wind_speed']
            result = {
                'city': city_name,
                'temperature': temp_celsius,
                'pressure': pressure_mm,
                'wind_speed': wind_speed
            }

            # Сохранение данных в кэше
            cache_data = {
                'cache_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'data': result
            }
            redis_client.set(cache_key, json.dumps(cache_data))

            return Response(result)
            # return Response(weather_data)
        else:
            return Response({'error': 'Failed to fetch weather data'},
                            status=500)
