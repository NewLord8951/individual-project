import os
import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher, executor
from dotenv import find_dotenv, load_dotenv
from private_chat import p_c
from group_chat import group_quiz
from channel import channel_joke
load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
CHANNEL_ID = os.getenv("CHANNEL_ID")

p_c(dp)
group_quiz(dp)
channel_joke(dp)
executor.start_polling(dp)


async def main():
    logger.add('file.log',
               format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
               rotation='3 days',
               backtrace=True,
               diagnose=True)
    logger.info('Бот запущен')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
