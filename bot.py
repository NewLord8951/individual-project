import os
import asyncio
from dotenv import load_dotenv, find_dotenv
from loguru import logger
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import requests
from bs4 import BeautifulSoup
from random import choice


load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")


async def main():
    logger.add("file.log",
               format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
               rotation="3 days",
               backtrace=True,
               diagnose=True)

    bot = Bot(token=TOKEN)
    logger.info("Бот создан")
    dp = Dispatcher()
    logger.info("Диспетчер создан")

    @dp.message(Command("start"))
    async def send_welcome(message: types.Message):
        await message.answer("Привет! Получи анекдот по команде: /anekdot")
        logger.info("Бот запущен")

    @dp.message(Command('anekdot'))
    async def send_anekdot(message: types.Message):
        response = requests.get('https://www.anekdot.ru/random/anekdot/')
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            jokes = soup.find_all('div', class_='text')

            random_joke = choice(jokes).text.strip()
            anekdot = random_joke
        else:
            anekdot = "Не удалось получить анекдот"

        await message.answer(anekdot)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
