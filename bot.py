import os
import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import find_dotenv, load_dotenv
from private_chat import register_private_handlers
from group_chat import setup_group_handlers, UserWarnings, WarningSystem
from channel import setup_channel_handlers, send_news

load_dotenv(find_dotenv())

logger.add("file.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")

storage = MemoryStorage()
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(storage=storage)


async def main():
    try:
        register_private_handlers(dp)
        setup_group_handlers(dp)
        setup_channel_handlers(dp, bot)
        send_news(dp)

        UserWarnings()
        WarningSystem(dp, bot)

        logger.info("Бот запущен")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
