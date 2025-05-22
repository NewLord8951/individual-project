from loguru import logger
from aiogram import Dispatcher, types, F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from reply import get_keyboard

router = Router()
scores = {}


class QuizState(StatesGroup):
    question_0 = State()
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()


async def send_question_0(message: types.Message, state: FSMContext):
    await state.set_state(QuizState.question_0)
    await message.answer(
        "Первый вопрос: блблблблб?",
        reply_markup=get_keyboard(
            "a0",
            "b0",
            "c0",
            "d0",
            placeholder="",
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
            placeholder="",
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
            placeholder="",
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
            placeholder="",
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
            placeholder="",
            sizes=(2, 2)
        ),
    )


def register_private_handlers(dp: Dispatcher):
    dp.include_router(router)

    @router.message(CommandStart(), F.chat.type == "private")
    async def cmd_start(message: types.Message, state: FSMContext):
        scores[message.from_user.id] = 0
        await message.answer('Здравствуйте! Бот запущен.')
        logger.info('Бот запущен')
        await send_question_0(message, state)

    @router.message(QuizState.question_0, F.chat.type == "private")
    async def handle_answer_0(message: types.Message, state: FSMContext):
        user_id = message.from_user.id

        if message.text in ["a0", "b0", "c0", "d0"]:
            await message.answer('ага')
            logger.info('Вопрос 1 написан')
            await send_question_1(message, state)
            if message.text == "c0":
                scores[user_id] += 1
        else:
            await message.answer("Что это??? Символы???")

    @router.message(QuizState.question_1, F.chat.type == "private")
    async def handle_answer_1(message: types.Message, state: FSMContext):
        user_id = message.from_user.id

        if message.text in ["a1", "b1", "c1", "d1"]:
            await message.answer('ага ясно')
            logger.info('Вопрос 2 написан')
            await send_question_2(message, state)
            if message.text == "a1":
                scores[user_id] += 1
        else:
            await message.answer("Что это??? Символы???")

    @router.message(QuizState.question_2, F.chat.type == "private")
    async def handle_answer_2(message: types.Message, state: FSMContext):
        user_id = message.from_user.id

        if message.text in ["a2", "b2", "c2", "d2"]:
            await message.answer('агась')
            logger.info('Вопрос 3 написан')
            await send_question_3(message, state)
            if message.text == "a2":
                scores[user_id] += 1
        else:
            await message.answer("Что это??? Символы???")

    @router.message(QuizState.question_3, F.chat.type == "private")
    async def handle_answer_3(message: types.Message, state: FSMContext):
        user_id = message.from_user.id

        if message.text in ["a3", "b3", "c3", "d3"]:
            await message.answer('да ну')
            logger.info('Вопрос 4 написан')
            await send_question_4(message, state)
            if message.text == "b3":
                scores[user_id] += 1
        else:
            await message.answer("Что это??? Символы???")

    @router.message(QuizState.question_4, F.chat.type == "private")
    async def handle_answer_4(message: types.Message, state: FSMContext):
        user_id = message.from_user.id

        if message.text in ["a4", "b4", "c4", "d4"]:
            await message.answer('пупупу')
            logger.info('Вопрос 5 написан')
            if message.text == "d4":
                scores[user_id] += 1

            if scores[user_id] == 1:
                a = "20%"
            elif scores[user_id] == 2:
                a = "40%"
            elif scores[user_id] == 3:
                a = "60%"
            elif scores[user_id] == 4:
                a = "80%"
            elif scores[user_id] == 5:
                a = "100%"

            await message.answer(f"Вы ответили правильно на: {a}")
            await state.clear()
        else:
            await message.answer("Что это??? Символы???")
