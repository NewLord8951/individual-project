import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from loguru import logger
from mat import contains_bad_words
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage

# Инициализация бота и хранилища
bot = Bot(token="YOUR_BOT_TOKEN")
storage = RedisStorage.from_url("redis://localhost:6379/0")
dp = Dispatcher(storage=storage)

class UserWarnings(StatesGroup):
    warning_1 = State()  # Первое предупреждение
    warning_2 = State()  # Второе предупреждение
    banned = State()     # Бан

STICKER_ID = "CAACAgIAAxkBAAEPHGZoJcDcrCtFMH4AAbcSPIzwcUP4x7cAAuBJAAJsvglLbTF7IeyHYuA2BA"
group_games = {}

# Настройка логгера
logger.add("debug.log", rotation="1 MB", level="DEBUG")

def setup_group_handlers(dp: Dispatcher):
    @dp.message(Command('start'), F.chat.type.in_({"group", "supergroup"}))
    async def start_game(message: types.Message):
        """Обработчик команды /start для начала игры"""
        chat_id = message.chat.id
        group_games[chat_id] = random.randint(1, 100)
        await message.answer(
            "🎮 Игра начата! Попробуй угадать число от 1 до 100.\n"
            "Используй команду /guess <число>"
        )
        logger.info(f"Игра начата в чате {chat_id}")

    @dp.message(Command('guess'), F.chat.type.in_({"group", "supergroup"}))
    async def make_guess(message: types.Message):
        """Обработчик команды /guess для попытки угадать число"""
        chat_id = message.chat.id
        
        # Проверка на маты в сообщении
        if contains_bad_words(message.text):
            await handle_bad_words(message)
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

    async def handle_bad_words(message: types.Message):
        """Обработчик матов в сообщениях"""
        user_id = message.from_user.id
        chat_id = message.chat.id
        
        # Получаем текущее состояние пользователя
        current_state = await dp.storage.get_state(chat=chat_id, user=user_id)
        
        if current_state == UserWarnings.warning_1.state:
            await dp.storage.set_state(chat=chat_id, user=user_id, state=UserWarnings.warning_2)
            await message.answer_sticker(STICKER_ID)
            await message.answer("🚨 Последнее предупреждение! Следующий мат — бан.")
            logger.warning(f"Второй мат от {user_id} в чате {chat_id}")
            
        elif current_state == UserWarnings.warning_2.state:
            await dp.storage.set_state(chat=chat_id, user=user_id, state=UserWarnings.banned)
            await message.answer_sticker(STICKER_ID)
            await bot.ban_chat_member(chat_id, user_id)
            await message.answer(f"⛔ Пользователь {message.from_user.full_name} забанен за маты.")
            logger.error(f"Бан пользователя {user_id} в чате {chat_id}")
            
        else:  # Первое нарушение
            await dp.storage.set_state(chat=chat_id, user=user_id, state=UserWarnings.warning_1)
            await message.answer_sticker(STICKER_ID)
            await message.answer("⚠️ Первое предупреждение! Следующее нарушение — бан.")
            logger.warning(f"Первый мат от {user_id} в чате {chat_id}")

    @dp.message(Command("reset_warnings"))
    async def reset_warnings(message: types.Message, state: FSMContext):
        """Сброс предупреждений для пользователя"""
        await state.clear()
        await message.answer("Ваши предупреждения сброшены.")
        logger.info(f"Сброс предупреждений для {message.from_user.id}")

# Запуск бота
if __name__ == "__main__":
    dp.run_polling(bot)