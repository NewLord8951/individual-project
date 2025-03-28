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
            "a0",
            "b0",
            "c0",
            "d0",
            placeholder="",
            sizes=(2, 2)
        ),
    )


@dp.message()
async def q0(message: types.Message):
    text = message.text

    if text in ["a0", "b0", "c0", "d0"]:
        await message.answer('ага')
        logger.info('Вопрос 1 написан')
        await message.answer(
            "Следующий вопрос гугугага?",
            reply_markup=get_keyboard(
                "a1",
                "b1",
                "c1",
                "d1",
                placeholder="",
                sizes=(2, 2)
            ),
        )
    else:
        await message.answer("Что это??? Символы???")


@dp.message()
async def q1(message: types.Message):
    text1 = ["a1", "b1", "c1", "d1"]

    if text1 in ["a1", "b1", "c1", "d1"]:
        await message.answer('ага ясно')
        logger.info('Вопрос 2 написан')
        await message.answer(
            "Следующий вопрос дадада??",
            reply_markup=get_keyboard(
                "a2",
                "b2",
                "c2",
                "d2",
                placeholder="",
                sizes=(2, 2)
            ),
        )
    else:
        await message.answer("Что это??? Символы???")


@dp.message()
async def q2(message: types.Message):
    text2 = ["a2", "b2", "c2", "d2"]

    if text2 in ["a2"]:
        await message.answer('агась')
    elif text2 in ["b2"]:
        await message.answer('агась')
    elif text2 in ["c2"]:
        await message.answer('агась')
    elif text2 in ["d2"]:
        await message.answer('агась')
    else:
        await message.answer("Что это??? Символы???")
    logger.info('Вопрос 3 написан')


async def main():
    logger.add('file.log',
               format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
               rotation='3 days',
               backtrace=True,
               diagnose=True)
    logger.info('Бот запущен')
    await dp.start_polling(bot)

asyncio.run(main())
