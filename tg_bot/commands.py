from aiogram import types
from logger.botLogger import botLogger
import requests
# from tg_bot.bot import send_poll
from tg_bot.bot import bot
from const import weather_interpretation
from config import PEXELS_API_KEY, CONVERSION_API
import random

from decorators import register_command, commands_dict
#init logger
logger = botLogger.getLogger(__name__)


@register_command(["start"])
async def start(message: types.Message):
    logger.warn(message.chat.id)
    await message.reply("Привет! Я твой бот. Что бы узнать что я умею напиши /help")


@register_command(["help"])
async def help(message: types.Message):
    await message.reply(message.chat.id, f"/weather Город - Выведет данные о погоде на данный момент в городе, который вы выставили, желательно писать город на английском языке(/weather Moscow)\n/convert Сумма С какой валюты На какую валюту(/convert 100 USD RUB)\n/image - Просто выводит картинку с милыми животными\n/polls Вопрос,Ответ,Ответ,итд - Отделение Вопроса/Ответов друг от друга происходит через запятую")


@register_command(["weather"])
async def get_weather(message: types.Message):
    city = message.text.replace('/weather ', "")
    try:
        # Get latitude and longitude by city
        search_param = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
         
        response = requests.get(search_param)
        req_json = response.json()
        
        found_city = req_json['results'][0]['name']
        latitude = req_json['results'][0]['latitude']
        longitude = req_json['results'][0]['longitude']
        logger.warn(message.chat.id)
    except Exception:
        return await message.reply(f"Город не найден, попробуйте еще раз в другом формате: /weather Город")
    
    # Get weather
    base_url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true'
    response = requests.get(base_url)
    
    if response.status_code != 200:
        return await message.reply(f"Произошла ошибка, попробуйте еще раз")
    
    req_json = response.json()
    

    return await message.reply(f"Город: {found_city}\nПогода сейчас: {weather_interpretation[req_json['current_weather']['weathercode']]}\nТемпература воздуха: {req_json['current_weather']['temperature']} °C\nСкорость ветра: {req_json['current_weather']['windspeed']} км/ч")


@register_command(["convert"])
async def convert_money(message: types.Message):
    money = message.text.replace('/convert ', "").split()  # split string into parts

    amount = float(money[0]) 
    from_currency = money[1]
    to_currency = money[2]
    try:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={to_currency}&from={from_currency}&amount={amount}"
        
        headers = {
            "apikey": CONVERSION_API
        }

        response = requests.request("GET", url, headers=headers)
        
        if response.status_code != 200:
            return await message.reply(f"Произошла ошибка, попробуйте еще раз")
        
        result = response.json()
        return await message.reply(f"Конвертация из {amount} {from_currency} в {to_currency}\nКурс 1 {from_currency} к {to_currency} = {result['info']['rate']}\nРезультат: {round(result['result'],2)} {to_currency}")
    
    except Exception:
        return await message.reply(f"Валюта не найдена, произошла ошибка, попробуйте ещё раз")

    


@register_command(["image"])
async def image_send(message: types.Message):
    # Doesn't work without proxy or vpn
    try:
        headers = {
            "Authorization": PEXELS_API_KEY
            }
        # Connect to proxy server
        proxies = {
            "https": f""
        }
        
        url = f"https://api.pexels.com/v1/search?query=cute_animals&per_page=1&page={random.randint(0, 100)}"
        
        response = requests.request("GET", url, headers=headers, proxies=proxies)
        
        if response.status_code != 200:
            if response.status_code == 522:
                return await message.reply(f"Произошла ошибка с запросом, обратитесь к разработчикам")
            return await message.reply(f"Произошла ошибка, попробуйте еще раз")
                
        result = response.json()

        return await message.reply(result['photos'][0]['src']['original'], disable_web_page_preview = False)
    except Exception:
        return await message.reply(f"Картинка не найдена, повторите попытку")


async def send_poll(chat_id, question, options):
    await bot.send_poll(chat_id=chat_id, question=question, options=options)


@register_command(["polls"])
async def create_polls(message: types.Message):
    parse_polls = message.text.replace('/polls ', "").split(",")  # split string into parts
    
    question = parse_polls[0]
    options = []
    
    #Parse split string and add options
    for option in parse_polls: options.append(option) if option != parse_polls[0] else None
    chat_id = options[-1]
    logger.warn(chat_id)
    options.remove(chat_id)
    try:
        return await send_poll(chat_id=chat_id, question=question, options=options)
    except Exception as e:
        return await message.reply(f"Не удалось создать опрос, попробуйте еще раз {e}")


#Registration all of the func
def setup(dispatcher):
    for key in commands_dict:
        func_name = globals()[key]
        dispatcher.register_message_handler(func_name, commands=commands_dict.get(key))

