import requests
import datetime
from config import token_bot, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=token_bot)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Да прибудет с Вами сила! Напишите название города и я пришлю сводку погоды.")


@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_time = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_time = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_od_sunday = datetime.datetime.fromtimestamp(data["sys"]["sunset"] - data["sys"]["sunrise"])

        await message.reply(f"Погода в городе: {city}\nТемпература: {cur_weather} °C\n"
                            f"Влажность: {humidity}\nАтмосферное давление: {pressure} мм.рт.ст\nСкорость ветра: {wind} м\с\n"
                            f"Восход солнца: {sunrise_time}\nЗакат: {sunset_time}\nСветовой день: {length_od_sunday}"
                            )
    except:
        await message.reply("Проверьте правильность написания города")


if __name__ == '__main__':
    executor.start_polling(dp)
