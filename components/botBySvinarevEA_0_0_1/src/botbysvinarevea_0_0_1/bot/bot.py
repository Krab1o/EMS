import logging

import telebot
from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, ReplyKeyboardRemove, User
from aiogram.types.callback_query import CallbackQuery
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile

from ..config import settings

bot = Bot(settings.BOT_TOKEN)
dp = Dispatcher()
telebot.logger.setLevel(logging.INFO)

authorized = []

users = {
    "admin@example.com": "admin",
    "user@example.com": "1234"
}

events_ = [
    {
        "title": "<b>Квест для первокурсников</b>\n\n"
                 "Интерактивная игра для новичков\n"
                 "Дата проведения: <b>15 ноября 2024г.</b>",
        "img": "img/people.jpg"
    },
    {
        "title": "<b>День рождения факультета</b>\n\n"
                 "Празднование дня рождения факультета\n"
                 "Дата проведения: <b>15 ноября 2024г.</b>",
        "img": "img/hackaton.jpg"
    },
    {
        "title": "<b>Студвесна</b>\n\n"
                 "Встреча нового учебного года\n"
                 "Дата проведения: <b>15 ноября 2024г.</b>",
        "img": "img/event.jpg"
    },
]

class Form(StatesGroup):
    credentials = State()
    events = State()

@dp.message(Form.credentials)
async def authorize(message: Message, state: FSMContext):
    username, password = message.text.split("/")
    if username not in users:
        await message.reply("Некорректные данные, повторите ввод: ")
    else:
        if password == users[username]:
            await state.clear()
            await state.set_state(Form.events)
            authorized.append(message.from_user.id)
            await message.reply(f"Успешная авторизация\N{smiling face with smiling eyes}!")
            await events(message, state)

@dp.message(Form.events)
async def events(message: Message, state: FSMContext):
    if message.from_user.id not in authorized:
        await state.set_state(Form.credentials)
        await message.reply("Введите данные учетной записи в формате: почта/пароль")
        await authorize(message, state)
    else:
        for event in events_:
            await bot.send_photo(message.chat.id, photo=FSInputFile(event["img"]), caption=event["title"], parse_mode='HTML')
    await state.clear()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    start = (f"Привет, {message.from_user.first_name}\N{winking face}!\n"
             "С помощью этого бота можно узнать информацию о мероприятиях и получать оповещение о предстоящих событиях.\n\n"
             f"Введите команду /help для получения списка доступных команд.")
    await message.answer(start)

@dp.message(Command("help"))
async def cmd_help(message: Message):
    kb = [
        [
            InlineKeyboardButton(text="Предстоящие события", callback_data = "events")
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer("Доступные команды:", reply_markup=keyboard)

@dp.callback_query()
async def cmd_events(call: CallbackQuery, state: FSMContext):
    if call.data == "events":
        await state.set_state(Form.events)
        await call.message.answer(await events(call.message, state), reply_markup=ReplyKeyboardRemove())