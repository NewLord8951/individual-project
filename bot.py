import os
import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher
from dotenv import find_dotenv, load_dotenv
from private_chat import (cmd_start, send_question_0,
                          handle_answer, send_question_1,
                          send_question_2, send_question_3, send_question_4)
from group_chat import group_quiz

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()
group_quiz(dp)
cmd_start(dp)
send_question_0(dp)
handle_answer(dp)
send_question_1(dp)
send_question_2(dp)
send_question_3(dp)
send_question_4(dp)


async def main():
    logger.add('file.log',
               format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
               rotation='3 days',
               backtrace=True,
               diagnose=True)
    logger.info('Бот запущен')
    await dp.start_polling(bot)

asyncio.run(main())
