import os
import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import find_dotenv, load_dotenv
from private_chat import p_c
from group_chat import setup_group_handlers, UserWarnings, WarningSystem
from channel import send_news, setup_channel_handlers

load_dotenv(find_dotenv())

storage = MemoryStorage()
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(storage=storage)


async def main():
    try:
        p_c(dp)
        setup_group_handlers(dp)
        UserWarnings(dp)
        send_news(dp)
        setup_channel_handlers(dp, bot)
        WarningSystem(dp, bot)

        logger.add("file.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")
        logger.info("Бот запущен")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
