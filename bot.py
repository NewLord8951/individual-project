import os
import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import find_dotenv, load_dotenv
from reply import get_keyboard

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer('Здравствуйте! Бот запущен.')
    logger.info('Бот запущен')
    await message.answer(
        "Первый вопрос: блблблблб?",
        reply_markup=get_keyboard(
            "a",
            "b",
            "c",
            "d",
            placeholder="",
            sizes=(2, 2)
        ),
    )


@dp.message()
async def eсho(message: types.Message):
    text = message.text

    if text in ["a", "b", "c", "d"]:
        await message.answer('ага')
        await message.answer(
            "Следующий вопрос гугугага?",
            reply_markup=get_keyboard(
                "1",
                "2",
                "3",
                "4",
                placeholder="",
                sizes=(2, 2)
            ),
        )
    else:
        await message.answer("Что это??? Символы???")


async def main():
    logger.add('file.log',
               format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
               rotation='3 days',
               backtrace=True,
               diagnose=True)
    logger.info('Бот запущен')
    await dp.start_polling(bot)

asyncio.run(main())
