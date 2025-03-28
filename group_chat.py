import random
from aiogram import Dispatcher, types, F
from aiogram.filters import Command
from loguru import logger

group_games = {}

logger.add("file_{time}.log")


def group_quiz(dp: Dispatcher):
    @dp.message(Command('start_game'), F.chat.type.in_({
        "group", "supergroup"}))
    async def start_game(message: types.Message):
        chat_id = message.chat.id
        group_games[chat_id] = random.randint(1, 100)
        await message.answer(
            "Игра начата! Угадай число от 1 до 100 (/guess N)")
        logger.info(f"Группа: игра в {chat_id}")

    @dp.message(Command('guess'), F.chat.type.in_({"group", "supergroup"}))
    async def make_guess(message: types.Message):
        chat_id = message.chat.id
        if chat_id not in group_games:
            await message.answer("Сначала /start_game")
            return

        try:
            guess = int(message.text.split()[1])
        except (IndexError, ValueError):
            await message.answer("Используйте: /guess 42")
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
