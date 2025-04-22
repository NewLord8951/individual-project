import os
import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher
from dotenv import find_dotenv, load_dotenv
from private_chat import p_c
from group_chat import setup_group_handlers
from channel import send_news, setup_channel_handlers
from mat import mats

load_dotenv(find_dotenv())

CHANNEL_ID = os.getenv("CHANNEL_ID")
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


async def main():
    try:
        p_c(dp)
        setup_group_handlers(dp)
        send_news(dp)
        setup_channel_handlers(dp, bot)
        mats(dp)

        logger.add('file.log',
                   format='{time:YYYY-MM-DD at HH:mm:ss} | {level} |\
                      {message}',
                   rotation='3 days',
                   backtrace=True,
                   diagnose=True)
        logger.info('Бот запущен')

        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f'Ошибка при запуске бота: {e}')

if __name__ == '__main__':
    asyncio.run(main())
