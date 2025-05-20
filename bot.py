import os
import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import find_dotenv, load_dotenv
from private_chat import register_private_handlers
from group_chat import setup_group_handlers, UserWarnings, WarningSystem
from channel import setup_channel_handlers, send_news
from database import init_db, add_user, add_warning, get_warnings


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


@dp.message_handler(commands=['warn'])
async def warn_user(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Ответьте на сообщение пользователя!")
        return

    target_user = message.reply_to_message.from_user
    admin = message.from_user
    reason = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""

    try:
        add_user(target_user.id, target_user.username, target_user.full_name)
        add_warning(target_user.id, admin.id, reason)

        warnings_count = get_warnings(target_user.id)
        response = (
            f"Пользователь {target_user.full_name} получил предупреждение "
            f"({warnings_count}/3). Причина: {reason or 'не указана'}"
        )
        await message.reply(response)
    except Exception as e:
        logger.error(f"Ошибка при добавлении предупреждения: {e}")
        await message.reply("Произошла ошибка при обработке запроса")


async def main():
    try:
        register_private_handlers(dp)
        setup_group_handlers(dp)
        setup_channel_handlers(dp, bot)

        user_warnings = UserWarnings(dp)
        warning_system = WarningSystem(dp, bot)
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
