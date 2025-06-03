from loguru import logger
from aiogram import Dispatcher, types, F, Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from reply import get_keyboard
from mat import contains_bad_words

router = Router()
scores = {}
STICKER_ID = "CAACAgIAAxkBAAEPHGZoJcDcrCtFMH4AAbcSPIzwcUP4x7cAAuBJAAJsvglLbTF7IeyHYuA2BA"


class QuizState(StatesGroup):
    question_0 = State()
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()


class UserWarningsPrivate(StatesGroup):
    """Класс состояний для системы предупреждений в приватном чате"""
    no_warning = State()
    first_warning = State()
    second_warning = State()
    banned = State()


class WarningSystemPrivate:
    def __init__(self, dp: Dispatcher, bot: Bot):
        self.dp = dp
        self.bot = bot
        self.register_handlers()

    def register_handlers(self):
        @self.dp.message(F.text & F.chat.type == "private")
        async def handle_private_messages(message: types.Message, state: FSMContext):
            quiz_state = await state.get_state()
            if quiz_state and quiz_state.startswith("QuizState:"):
                return

            current_warning_state = await state.get_state()
            if current_warning_state == UserWarningsPrivate.banned.state:
                await message.answer("⛔ Вы заблокированы и не можете использовать бота")
                return

            if contains_bad_words(message.text.lower()):
                if current_warning_state == UserWarningsPrivate.first_warning.state:
                    await state.set_state(UserWarningsPrivate.second_warning)
                    await message.answer_sticker(STICKER_ID)
                    await message.answer("🚨 Последнее предупреждение! Следующее нарушение приведет к блокировке.")
                    logger.warning(f"Пользователь {message.from_user.id} получил второе предупреждение")

                elif current_warning_state == UserWarningsPrivate.second_warning.state:
                    await state.set_state(UserWarningsPrivate.banned)
                    await message.answer_sticker(STICKER_ID)
                    await message.answer("⛔ Вы заблокированы за нарушение правил!")
                    logger.error(f"Пользователь {message.from_user.id} заблокирован")  

                else:
                    await state.set_state(UserWarningsPrivate.first_warning)
                    await message.answer_sticker(STICKER_ID)
                    await message.answer("⚠️ Первое предупреждение! Пожалуйста, соблюдайте правила общения.")
                    logger.warning(f"Пользователь {message.from_user.id} получил первое предупреждение")


def register_private_handlers(dp: Dispatcher, bot: Bot):
    dp.include_router(router)

    async def check_banned(message: types.Message, state: FSMContext) -> bool:
        """Проверяет, забанен ли пользователь"""
        current_state = await state.get_state()
        if current_state == UserWarningsPrivate.banned.state:
            await message.answer("⛔ Вы заблокированы и не можете использовать бота")
            return True
        return False

    @router.message(Command('start'), F.chat.type == "private")
    async def cmd_start(message: types.Message, state: FSMContext):
        if await check_banned(message, state):
            return

        scores[message.from_user.id] = 0
        await state.set_state(UserWarningsPrivate.no_warning)
        await message.answer('Добро пожаловать! Начнем викторину.')
        logger.info(f'Пользователь {message.from_user.id} начал викторину')
        await send_question_0(message, state)

    @router.message(QuizState.question_0, F.chat.type == "private")
    async def handle_answer_0(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state == UserWarningsPrivate.banned.state:
            return

        user_id = message.from_user.id

        if message.text in ["a0", "b0", "c0", "d0"]:
            await message.answer('Спасибо за ответ!')
            logger.info(f'Пользователь {user_id} ответил на вопрос 0')
            await send_question_1(message, state)
            if message.text == "c0":
                scores[user_id] += 1
                logger.info(f'Пользователь {user_id} дал правильный ответ')
        else:
            await message.answer("Пожалуйста, используйте кнопки для ответа")

    @router.message(QuizState.question_1, F.chat.type == "private")
    async def handle_answer_1(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state == UserWarningsPrivate.banned.state:
            return

        user_id = message.from_user.id

        if message.text in ["a1", "b1", "c1", "d1"]:
            await message.answer('Ответ принят!')
            logger.info(f'Пользователь {user_id} ответил на вопрос 1')
            await send_question_2(message, state)
            if message.text == "a1":
                scores[user_id] += 1
                logger.info(f'Пользователь {user_id} дал правильный ответ')
        else:
            await message.answer("Пожалуйста, используйте кнопки для ответа")

    @router.message(QuizState.question_2, F.chat.type == "private")
    async def handle_answer_2(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state == UserWarningsPrivate.banned.state:
            return

        user_id = message.from_user.id

        if message.text in ["a2", "b2", "c2", "d2"]:
            await message.answer('Отлично! Продолжаем.')
            logger.info(f'Пользователь {user_id} ответил на вопрос 2')
            await send_question_3(message, state)
            if message.text == "a2":
                scores[user_id] += 1
                logger.info(f'Пользователь {user_id} дал правильный ответ')
        else:
            await message.answer("Пожалуйста, используйте кнопки для ответа")

    @router.message(QuizState.question_3, F.chat.type == "private")
    async def handle_answer_3(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state == UserWarningsPrivate.banned.state:
            return

        user_id = message.from_user.id

        if message.text in ["a3", "b3", "c3", "d3"]:
            await message.answer('Хороший ответ!')
            logger.info(f'Пользователь {user_id} ответил на вопрос 3')
            await send_question_4(message, state)
            if message.text == "b3":
                scores[user_id] += 1
                logger.info(f'Пользователь {user_id} дал правильный ответ')
        else:
            await message.answer("Пожалуйста, используйте кнопки для ответа")

    @router.message(QuizState.question_4, F.chat.type == "private")
    async def handle_answer_4(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state == UserWarningsPrivate.banned.state:
            return

        user_id = message.from_user.id

        if message.text in ["a4", "b4", "c4", "d4"]:
            await message.answer('Спасибо за участие!')
            logger.info(f'Пользователь {user_id} ответил на вопрос 4')
            if message.text == "d4":
                scores[user_id] += 1
                logger.info(f'Пользователь {user_id} дал правильный ответ')

            result = {
                1: "20%",
                2: "40%",
                3: "60%",
                4: "80%",
                5: "100%"
            }.get(scores[user_id], "0%")

            await message.answer(f"🎉 Ваш результат: {result} правильных ответов!")
            await state.set_state(UserWarningsPrivate.no_warning)
        else:
            await message.answer("Пожалуйста, используйте кнопки для ответа")


async def send_question_0(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == UserWarningsPrivate.banned.state:
        await message.answer("⛔ Вы заблокированы и не можете участвовать в викторине")
        return

    await state.set_state(QuizState.question_0)
    await message.answer(
        "Первый вопрос: блблблблб?",
        reply_markup=get_keyboard(
            "a0",
            "b0",
            "c0",
            "d0",
            placeholder="Выберите ответ:",
            sizes=(2, 2)
        ),
    )


async def send_question_1(message: types.Message, state: FSMContext):
    await state.set_state(QuizState.question_1)
    await message.answer(
        "Следующий вопрос гугугага?",
        reply_markup=get_keyboard(
            "a1",
            "b1",
            "c1",
            "d1",
            placeholder="Выберите ответ:",
            sizes=(2, 2)
        ),
    )


async def send_question_2(message: types.Message, state: FSMContext):
    await state.set_state(QuizState.question_2)
    await message.answer(
        "Следующий вопрос дадада??",
        reply_markup=get_keyboard(
            "a2",
            "b2",
            "c2",
            "d2",
            placeholder="Выберите ответ:",
            sizes=(2, 2)
        ),
    )


async def send_question_3(message: types.Message, state: FSMContext):
    await state.set_state(QuizState.question_3)
    await message.answer(
        "Следующий вопрос лингангу??",
        reply_markup=get_keyboard(
            "a3",
            "b3",
            "c3",
            "d3",
            placeholder="Выберите ответ:",
            sizes=(2, 2)
        ),
    )


async def send_question_4(message: types.Message, state: FSMContext):
    await state.set_state(QuizState.question_4)
    await message.answer(
        "Следующий вопрос гулигули??",
        reply_markup=get_keyboard(
            "a4",
            "b4",
            "c4",
            "d4",
            placeholder="Выберите ответ:",
            sizes=(2, 2)
        ),
    )
