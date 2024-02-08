# About WEATHER_API
API, которое на HTTP-запрос GET /weather?city=<city_name>,
где <city_name> - это название города на русском языке,
возвращает текущую температуру в этом городе в градусах Цельсия,
атмосферное давление (мм рт.ст.) и скорость ветра (м/с).
При первом запросе, сервис должен получать данные о погоде от yandex,
при последующих запросах для этого города в течение получаса запросы
на сервис yandex происходить не должны.
БОНУС: телеграмм-бот который работает с этим API

# Stack
- Python 3.10
- Django==5.0.2
- djangorestframework==3.14.0
- Redis
- aiogram
- more info in requirements.py 


# To start working development DRF

1. стяни ветку мастер - pull master from github
2. не забудь установить redis для кеширования прогноза погоды - don't foget install redis и зависимости pip install -r requirements.txt
3. создай базу, проведи миграции - python manage.py makemigrations, python manage.py migrate
4. ипортируй в базу список городов из файла cities.csv -  python manage.py importcities 
6. создай файл .env с твоими переменными и ключами для settings, смотри образец .sample file to set you settings, you can check .env_sample file
7. запусти redis - in terminal start redis: redis-server
8. запусти django server - in terminal start servise: python manage.py runserver
9. пользуйся - http://127.0.0.1:8000/ or http://127.0.0.1:8000/swagger/ 
10. пример запроса: http://127.0.0.1:8000/weather?city=Курск

# To start working telegram bot
11. после запуска redis и django-server можно запустить telegram bot
12. создай бота в телеграм @BotFather и добавь токен в файл .evn
13. запусти бота python t_bot_ya_weather.py
    

# TODO:
- есть потенциально баг, в базе берётся первый совпавший город,
 а города в России часто имеют одинаковое название, нужно добавить
 чтобы ещё и область/край спрашивало, если нашло более одного города
