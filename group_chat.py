import random
import re
from aiogram import Dispatcher, types, F
from aiogram.filters import Command
from loguru import logger
from mat import mats

STICKER_ID = "CAACAgIAAxkBAAEPHGZoJcDcrCtFMH4AAbcSPIzwcUP4x7cAAuBJAAJsvglLbTF7IeyHYuA2BA"


group_games = {}

logger.add("debug.log", rotation="1 MB", level="DEBUG")


def setup_group_handlers(dp: Dispatcher):
    @dp.message(Command('start'), F.chat.type.in_({"group", "supergroup"}))
    async def start_game(message: types.Message):
        """Обработчик команды /start для начала игры"""
        chat_id = message.chat.id
        group_games[chat_id] = random.randint(1, 100)
        await message.answer("🎮 Игра начата! Попробуй угадать число от 1 до 100.\n"
                           "Используй команду /guess <число>")
        logger.info(f"Игра начата в чате {chat_id}")

    @dp.message(Command('guess'), F.chat.type.in_({"group", "supergroup"}))
    async def make_guess(message: types.Message):
        """Обработчик команды /guess для попытки угадать число"""
        chat_id = message.chat.id

        if any(re.search(rf'\b{re.escape(word)}\b', message.text, re.IGNORECASE) 
               for word in mats):
            await message.answer_sticker(STICKER_ID)
            logger.warning(f"Обнаружены маты в чате {chat_id}")
            return

        if chat_id not in group_games:
            await message.answer("Сначала начните игру командой /start")
            return

        try:
            guess = int(message.text.split()[1])
        except (IndexError, ValueError):
            await message.answer("❌ Неправильный формат. Используйте: /guess 42")
            return

        secret = group_games[chat_id]

        if guess < secret:
            await message.answer("🔺 Мое число больше!")
        elif guess > secret:
            await message.answer("🔻 Мое число меньше!")
        else:
            await message.answer(f"🎉 Поздравляю! Ты угадал число {secret}!")
            del group_games[chat_id]
            logger.info(f"Игра завершена в чате {chat_id}")
