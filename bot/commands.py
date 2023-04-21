from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import ParseMode
from logger.botLogger import botLogger
import requests
from const import weather_interpretation

from decorators import register_command, commands_dict
logger = botLogger.getLogger(__name__)


@register_command(["start"])
async def start(message: types.Message):
    await message.answer("Привет! Я твой бот. Что бы узнать что я умею напиши /help")


@register_command(["weather"])
async def weather(message: types.Message):
    city = message.text.replace('/weather ', "")
    try:
        search_param = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        response = requests.get(search_param)
        req_json = response.json()
    
        latitude = req_json['results'][0]['latitude']
        longitude = req_json['results'][0]['longitude']
    except Exception:
        return await message.answer(f"Город не найден, попробуйте еще раз в другой формате")
        
    
    base_url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true'
    response = requests.get(base_url)
    req_json = response.json()
    

    return await message.answer(f"Погода сейчас: {weather_interpretation[req_json['current_weather']['weathercode']]}\nТемпература воздуха: {req_json['current_weather']['temperature']} °C\nСкорость ветра: {req_json['current_weather']['windspeed']} км/ч")


def setup(dispatcher):
    logger.warn(commands_dict)
    for key in commands_dict:
        func_name = globals()[key]
        dispatcher.register_message_handler(func_name, commands=commands_dict.get(key))
    # for key in commands_dict:
        

