import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import find_dotenv, load_dotenv
from loguru import logger

load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Этот quiz по географии пишите всё с маленькой буквы:\
                         Первый вопрос: Столица Аргентины?")


@dp.message()
async def convers(message: types.Message):
    if message.text == "буэнос-айрес":
        await message.answer("Правильно")
    elif message.text == "Буэнос Айрес":
        await message.answer("Я же просил")
    else:
        await message.answer("Не правильно")


async def main():
    await dp.start_polling(bot)

asyncio.run(main())
