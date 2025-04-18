import random
import re
from aiogram import Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from loguru import logger
from mat import mats

bad_words = mats
sticker_id = "5407062198700755424"
group_games = {}

logger.add("file_{time}.log")


def group_quiz(dp: Dispatcher):
    @dp.message(CommandStart(), F.chat.type.in_({"group", "supergroup"}))
    async def start_game(message: types.Message):
        chat_id = message.chat.id
        group_games[chat_id] = random.randint(1, 100)
        await message.answer("Игра начата! Угадай число от 1 до 100 (/guess N)")
        logger.info(f"Группа: игра начата в {chat_id}")

    @dp.message(Command('guess'), F.chat.type.in_({"group", "supergroup"}))
    async def make_guess(message: types.Message):
        chat_id = message.chat.id

        if chat_id not in group_games:
            await message.answer("Сначала начните игру с помощью /guess")
            return

        if any(re.search(rf'\b{word}\b', message.text, re.IGNORECASE) for word in bad_words):
            await message.answer_sticker(sticker_id)
            await message.answer("Пожалуйста, не используйте грубые слова!")
            return

        try:
            guess = int(message.text.split()[1])
        except (IndexError, ValueError):
            await message.answer("Используйте: /guess N (где N - ваше предположение)")
            return

        secret = group_games[chat_id]

        if guess < secret:
            await message.answer("Я загадал число больше!")
        elif guess > secret:
            await message.answer("Я загадал число меньше!")
        else:
            await message.answer(f"Угадал! Это {secret}")
            del group_games[chat_id]
            logger.info(f"Группа: игра завершена в {chat_id}")
