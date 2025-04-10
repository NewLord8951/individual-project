import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from loguru import logger
from bs4 import BeautifulSoup
from random import choice

logger.add("file_{time}.log")


async def get_random_joke():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.anekdot.ru/random/anekdot/") as response:
                if response.status == 200:
                    text = await response.text()
                    soup = BeautifulSoup(text, 'html.parser')
                    jokes = soup.find_all('div', class_='text')
                    if jokes:
                        return choice(jokes).text.strip()
                    return "Не удалось найти анекдот на странице"
                return "Не удалось получить анекдот"
    except Exception as e:
        logger.error(f"Ошибка при получении анекдота: {e}")
        return "Ошибка при получении анекдота"


async def send_jokes_periodically(bot: Bot, chat_id: int):
    while True:
        joke = await get_random_joke()
        logger.info(f"Бот рассказал: {joke}")
        try:
            await bot.send_message(chat_id, joke)
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения: {e}")
        await asyncio.sleep(30)


def channel_joke(dp: Dispatcher):
    @dp.message(Command('start'), F.chat.type.in_({"channel"}))
    async def start_jokes(message: Message):
        asyncio.create_task(send_jokes_periodically(message.bot, message.chat.id))
        await message.answer("Начинаю отправку анекдотов каждые 30 секунд!")
