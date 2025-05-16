import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from loguru import logger
from mat import contains_bad_words
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from dotenv import find_dotenv, load_dotenv

STICKER_ID = "CAACAgIAAxkBAAEPHGZoJcDcrCtFMH4AAbcSPIzwcUP4x7cAAuBJAAJsvglLbTF7IeyHYuA2BA"
group_games = {}

load_dotenv(find_dotenv())

logger.add("debug.log", rotation="1 MB", level="DEBUG")


class UserWarnings(StatesGroup):
    """Класс состояний для системы предупреждений"""
    no_warning = State()
    first_warning = State()
    second_warning = State()
    banned = State()


class WarningSystem:
    def __init__(self, dp: Dispatcher, bot: Bot):
        self.dp = dp
        self.bot = bot
        self.register_handlers()

    def register_handlers(self):
        self.dp.message.register(
            self.handle_bad_words, 
            F.text & F.chat.type.in_({"group", "supergroup"})
        )

    async def handle_bad_words(self, message: types.Message, state: FSMContext):
        if contains_bad_words(message.text):
            current_state = await state.get_state()

            if current_state == UserWarnings.first_warning.state:
                await state.set_state(UserWarnings.second_warning)
                await message.answer_sticker(STICKER_ID)
                await message.answer("🚨 Последнее предупреждение! Следующий мат — бан.")
                logger.warning(f"Второй мат от {message.from_user.id}")

            elif current_state == UserWarnings.second_warning.state:
                await state.set_state(UserWarnings.banned)
                await message.answer_sticker(STICKER_ID)
                await self.bot.ban_chat_member(
                    chat_id=message.chat.id,
                    user_id=message.from_user.id
                )
                await message.answer(f"⛔ Пользователь {message.from_user.full_name} забанен!")
                logger.error(f"Бан пользователя {message.from_user.id}")

            else:
                await state.set_state(UserWarnings.first_warning)
                await message.answer_sticker(STICKER_ID)
                await message.answer("⚠️ Первое предупреждение!")
                logger.warning(f"Первое предупреждение для {message.from_user.id}")


def setup_group_handlers(dp: Dispatcher):
    @dp.message(Command('start'), F.chat.type.in_({"group", "supergroup"}))
    async def start_game(message: types.Message):
        chat_id = message.chat.id
        group_games[chat_id] = random.randint(1, 100)
        await message.answer(
            "🎮 Игра начата! Угадай число от 1 до 100.\n"
            "Используй /guess <число>"
        )
        logger.info(f"Игра начата в чате {chat_id}")

    @dp.message(Command('guess'), F.chat.type.in_({"group", "supergroup"}))
    async def make_guess(message: types.Message):
        chat_id = message.chat.id

        if chat_id not in group_games:
            await message.answer("Сначала начните игру командой /start")
            return

        try:
            guess = int(message.text.split()[1])
        except (IndexError, ValueError):
            await message.answer("❌ Используйте: /guess 42")
            return

        secret = group_games[chat_id]

        if guess < secret:
            await message.answer("🔺 Больше!")
        elif guess > secret:
            await message.answer("🔻 Меньше!")
        else:
            await message.answer(f"🎉 Ты угадал число {secret}!")
            del group_games[chat_id]
            logger.info(f"Игра завершена в чате {chat_id}")

    @dp.message(Command("reset_warnings"))
    async def reset_warnings(message: types.Message, state: FSMContext):
        await state.clear()
        await message.answer("Предупреждения сброшены.")
        logger.info(f"Сброс предупреждений для {message.from_user.id}")
