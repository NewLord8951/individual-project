import os
import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import find_dotenv, load_dotenv

from private_chat import register_private_handlers
from group_chat import setup_group_handlers
from channel import setup_channel_handlers, send_news
from database import init_db

load_dotenv(find_dotenv())

logger.add(
    "logs/bot.log",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    rotation="10 MB",
    retention="30 days",
    compression="zip"
)


async def setup_bot():
    """Инициализация и настройка бота"""
    if not (token := os.getenv('TOKEN')):
        logger.error("Токен бота не найден в переменных окружения!")
        raise ValueError("Токен бота не установлен")

    try:
        init_db()
        logger.info("База данных успешно инициализирована")
    except Exception as e:
        logger.error(f"Ошибка инициализации БД: {e}")
        raise

    bot = Bot(token=token)
    dp = Dispatcher(storage=MemoryStorage())

    try:
        register_private_handlers(dp, bot)
        setup_group_handlers(dp)
        setup_channel_handlers(dp, bot)
        logger.info("Все обработчики успешно зарегистрированы")
    except Exception as e:
        logger.error(f"Ошибка регистрации обработчиков: {e}")
        raise

    asyncio.create_task(send_news(bot))
    logger.info("Фоновые задачи запущены")

    return bot, dp


async def main():
    """Основная функция запуска бота"""
    try:
        bot, dp = await setup_bot()
        logger.info("Бот успешно настроен и запускается...")

        await bot.delete_webhook(drop_pending_updates=True)

        await dp.start_polling(bot)
    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}")
    finally:
        if 'bot' in locals():
            await bot.session.close()
        logger.info("Бот остановлен")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен по запросу пользователя")
    except Exception as e:
        logger.critical(f"Необработанная ошибка: {e}")
