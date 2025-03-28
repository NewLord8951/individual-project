import os
import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import find_dotenv, load_dotenv
from reply import get_keyboard

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

user_states = {}
scores = {}


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    user_states[message.from_user.id] = 0
    scores[message.from_user.id] = 0
    await message.answer('Здравствуйте! Бот запущен.')
    logger.info('Бот запущен')
    await send_question_0(message)


async def send_question_0(message: types.Message):
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


@dp.message()
async def handle_answer(message: types.Message):
    user_id = message.from_user.id
    current_question = user_states.get(user_id)

    if current_question == 0:
        if message.text in ["a0", "b0", "c0", "d0"]:
            await message.answer('ага')
            logger.info('Вопрос 1 написан')
            user_states[user_id] = 1
            await send_question_1(message)
            if message.text == "c0":
                scores[user_id] += 1
        else:
            await message.answer("Что это??? Символы???")

    elif current_question == 1:
        if message.text in ["a1", "b1", "c1", "d1"]:
            await message.answer('ага ясно')
            logger.info('Вопрос 2 написан')
            user_states[user_id] = 2
            await send_question_2(message)
            if message.text == "a1":
                scores[user_id] += 1
        else:
            await message.answer("Что это??? Символы???")

    elif current_question == 2:
        if message.text in ["a2", "b2", "c2", "d2"]:
            await message.answer('агась')
            logger.info('Вопрос 3 написан')
            user_states[user_id] = 3
            await send_question_3(message)
            if message.text == "a2":
                scores[user_id] += 1
        else:
            await message.answer("Что это??? Символы???")

    elif current_question == 3:
        if message.text in ["a3", "b3", "c3", "d3"]:
            await message.answer('да ну')
            logger.info('Вопрос 4 написан')
            user_states[user_id] = 4
            await send_question_4(message)
            if message.text == "b3":
                scores[user_id] += 1
        else:
            await message.answer("Что это??? Символы???")

    elif current_question == 4:
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
        else:
            await message.answer("Что это??? Символы???")


async def send_question_1(message: types.Message):
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


async def send_question_2(message: types.Message):
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


async def send_question_3(message: types.Message):
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


async def send_question_4(message: types.Message):
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


async def main():
    logger.add('file.log',
               format='{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}',
               rotation='3 days',
               backtrace=True,
               diagnose=True)
    logger.info('Бот запущен')
    await dp.start_polling(bot)

asyncio.run(main())
