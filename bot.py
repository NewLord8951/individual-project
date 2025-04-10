import os
import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher
from dotenv import find_dotenv, load_dotenv
from private_chat import p_c
from group_chat import group_quiz
from channel import send_jokes_task, setup_channel_handlers

load_dotenv(find_dotenv())

CHANNEL_ID = os.getenv("CHANNEL_ID")
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


async def main():
    try:
        p_c(dp)
        group_quiz(dp)
        send_jokes_task(dp)
        setup_channel_handlers(dp, bot)

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
