#Add repository for python visibility
import sys
sys.path.append('')

from config import TELEGRAM_TOKEN
from aiogram import Bot, Dispatcher, executor
import commands

bot = Bot(token=TELEGRAM_TOKEN)

dp = Dispatcher(bot)

commands.setup(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

