# Телеграм бот, который взаимодействует с нашим API
import os
from pathlib import Path
from dotenv import load_dotenv

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram import types
import asyncio

import requests

# Загрузка переменных
dot_env = ".env"
load_dotenv(dotenv_path=dot_env)
# Установка токена телеграм-бота
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# URL API погоды на DRF
API_URL = os.getenv("API_URL_FOR_TELEGRAM_BOT")

# Создание экземпляра бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


# Создание состояния
class UserState(StatesGroup):
    city = State()


@dp.message_handler(Command('start'))
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Погода')
    await message.answer("Привет. Я бот прогноза погоды от Yandex. Напиши Погода или воспользуйся кнопкой в меню.",
                         reply_markup=keyboard)


# Обработчик текстового сообщения ‘Погода’
@dp.message_handler(text='Погода')
async def buy(message: types.Message):
    await message.answer('Напиши город в котором хочешь узнать погоду:')
    # Отправленный пользователем ответ будет сохранён
    await UserState.city.set()


@dp.message_handler(state=UserState.city)
async def fsm_handler(message: types.Message, state: FSMContext):
    # Получаем введённый юзером город и добавляем в машину состояний
    await state.update_data(city=message.text)
    data = await state.get_data()
    # Делаем запрос к нашему API на DRF
    response = requests.get(f"{API_URL}/weather?city={data['city']}")
    data = response.json()
    # Отвечаем на сообщение с указанием введенного города
    if 'error' in data:
        await message.answer(data['error'])
    else:
        city = data.get('city')
        temperature = data.get('temperature')
        pressure = data.get('pressure')
        wind_speed = data.get('wind_speed')
        if city and temperature and pressure and wind_speed:
            weather_info = f"Информация о погоде в городе {city}:\n\n"
            weather_info += f"Температура: {temperature}°C\n"
            weather_info += f"Давление: {pressure} гПа\n"
            weather_info += f"Скорость ветра: {wind_speed} м/с"
            await message.answer(weather_info)
        else:
            await message.answer("Не удалось получить информацию о погоде.")
    # Закрываем машину состояний
    await state.finish()


# Вызов функции запуска бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
