#Add repository for python visibility
import sys
sys.path.append('')

from config import TELEGRAM_TOKEN
from aiogram import Bot, Dispatcher, executor

bot = Bot(token=TELEGRAM_TOKEN)


dp = Dispatcher(bot)


if __name__ == '__main__':
    from tg_bot.commands import setup
    setup(dp)
    executor.start_polling(dp, skip_updates=True)

