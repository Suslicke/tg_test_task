import sys
sys.path.append('/Users/suslicketeam/Documents/Programming/Python/telegram_bot_test_task')

from config import TELEGRAM_TOKEN, WEATHER_TOKEN, WEBHOOK_URL
from aiogram import Bot, Dispatcher, executor
from logger.botLogger import botLogger
import commands
logger = botLogger.getLogger(__name__)

bot = Bot(token=TELEGRAM_TOKEN)

dp = Dispatcher(bot)

commands.setup(dp)
# commands.register_commands(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

