import os
import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import find_dotenv, load_dotenv
from private_chat import register_private_handlers
from group_chat import setup_group_handlers, UserWarnings, WarningSystem
from channel import setup_channel_handlers, send_news
from database import init_db


load_dotenv(find_dotenv())
init_db()

logger.add(
    "file.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    rotation="10 MB",
    retention="30 days"
)

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(storage=MemoryStorage())


async def main():
    try:
        register_private_handlers(dp)
        setup_group_handlers(dp)
        setup_channel_handlers(dp, bot)

        UserWarnings()
        WarningSystem(dp, bot)
        asyncio.create_task(send_news(bot))

        logger.info("Бот запущен")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        await (await bot.get_session()).close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен вручную")
    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}")
