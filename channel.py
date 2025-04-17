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
    news_list = []
    index = 0

    while True:
        try:
            if not news_list or index >= len(news_list):
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://www.rbc.ru/") as response:
                        if response.status == 200:
                            text = await response.text()
                            soup = BeautifulSoup(text, "html.parser")
                            news_spans = soup.find_all("span", class_="main__feed__title-wrap")
                            news_list = [i.text.strip() for i in news_spans if i.text.strip()]
                            index = 0
                            if not news_list:
                                logger.warning("Канал: новости не найдены на странице")
                                await asyncio.sleep(100)
                                continue
                        else:
                            logger.warning(f"Канал: проблема с сайтом новостей, статус {response.status}")
                            await asyncio.sleep(100)
                            continue

            current_news = news_list[index]
            await bot.send_message(CHANNEL_ID, f"Новость:\n{current_news}")
            logger.success(f"Канал: новость отправлена ({index + 1}/{len(news_list)})")

            index += 1

        except Exception as e:
            logger.error(f"Канал: ошибка {e}")

        await asyncio.sleep(100)


def setup_channel_handlers(dp: Dispatcher, bot: Bot):
    asyncio.create_task(send_news(bot))

    @dp.message(Command('channel_stats'), F.chat.type == "channel")
    async def channel_stats(message: types.Message):
        await message.answer("Бот канала работает!")
        logger.info("Канал: проверка работы")
