import os
import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher
from dotenv import find_dotenv, load_dotenv
from private_chat import p_c
from group_chat import group_quiz
from channel import channel_joke, get_random_joke, send_jokes_periodically
load_dotenv(find_dotenv())

CHANNEL_ID = os.getenv("CHANNEL_ID")
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


async def main():
    p_c(dp)
    group_quiz(dp)
    channel_joke(dp)
    get_random_joke(dp)
    send_jokes_periodically(dp)

    logger.add('file.log',
               format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
               rotation='3 days',
               backtrace=True,
               diagnose=True)
    logger.info('Бот запущен')

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
