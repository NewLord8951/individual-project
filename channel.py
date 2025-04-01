import asyncio
import requests
from aiogram import Dispatcher, types, F
from aiogram.filters import Command
from loguru import logger
from bs4 import BeautifulSoup
from random import choice

logger.add("file_{time}.log")


def channel_joke(dp: Dispatcher):
    @dp.message(Command('a'), F.chat.type.in_({"channel"}))
    async def send_random_joke(message: types.Message):
        while True:
            try:
                response = requests.get(
                    "https://www.anekdot.ru/random/anekdot/")
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    jokes = soup.find_all('div', class_='text')
                    random_joke = choice(jokes).text.strip()
                    anekdot = random_joke
                else:
                    anekdot = 'Не удалось получить анекдот'

                logger.info(f"Бот рассказал: {anekdot}")

                await message.answer(anekdot)
            except Exception as e:
                logger.error(f"Ошибка при отправке сообщения: {e}")

            await asyncio.sleep(30)
