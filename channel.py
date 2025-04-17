import aiohttp
import asyncio
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from loguru import logger
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
CHANNEL_ID = os.getenv("CHANNEL_ID")


async def send_news(bot: Bot):
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.rbc.ru/") as response:
                    if response.status == 200:
                        text = await response.text()
                        soup = BeautifulSoup(text, "html.parser")
                        news = soup.find_all("span", class_="main__feed__title-wrap")
                        if news:
                            new_0 = [i.text + "\n" for i in news]
                            await bot.send_message(CHANNEL_ID, f"Новость:\n{new_0}")
                            logger.success("Канал: новость отправлена")
                        else:
                            logger.warning("Канал: новости не найдены на странице")
                    else:
                        logger.warning(f"Канал: проблема с сайтом новостей, статус {response.status}")
        except Exception as e:
            logger.error(f"Канал: ошибка {e}")

        await asyncio.sleep(100)


def setup_channel_handlers(dp: Dispatcher, bot: Bot):
    asyncio.create_task(send_news(bot))

    @dp.message(Command('channel_stats'), F.chat.type == "channel")
    async def channel_stats(message: types.Message):
        await message.answer("Бот канала работает!")
        logger.info("Канал: проверка работы")
