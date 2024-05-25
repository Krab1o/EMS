import asyncio
import json
import logging
from aiogram import Router
import telebot
from aiogram import F
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram import types
from aiogram.types import URLInputFile
from aiogram.types.callback_query import CallbackQuery
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import requests
from datetime import datetime


BASE_URL = "http://api.evgenym.com"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHAiOjE3MTY3MDk4NzF9.3yE1mM_Y363abPsGQ_g3CbIuhDvV_rJR9o3ZQ_caXDM"
bot = Bot("6755807133:AAEy_rjRuTj3ePbLlvFW-Ly1aO8CoIQDDy8")

telebot.logger.setLevel(logging.INFO)

router = Router()

dp = Dispatcher()
dp.include_routers(router)

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


class BOT_STATE(StatesGroup):
    no_auth = State()
    auth = State()


@router.message(StateFilter(None), Command('start'))
async def send_welcome(message: types.Message):
    start = (f"Привет, {message.from_user.first_name}\N{winking face}!\n"
             "С помощью этого бота можно узнать информацию о мероприятиях и получать оповещение о предстоящих событиях.\n\n"
             "Бот доступен только для зарегестрированных пользователей")
    kb = [
        [types.InlineKeyboardButton(text="Авторизоваться", callback_data="auth")]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer(start, reply_markup=keyboard)


@router.callback_query(F.data == "auth")
async def get_credentials(call: CallbackQuery, state: FSMContext):
    await call.message.answer(
        text="Введите почта/пароль",
    )
    await state.set_state(BOT_STATE.no_auth)


@router.message(
    BOT_STATE.no_auth,
)
async def credentials_sended(message: types.Message, state: FSMContext):
    email, password = message.text.split("/")
    response = await send_auth_request(email, password, message.from_user.id)
    print(response)
    if (response != 'error'):
        await state.update_data(user_id=response['user_id'])
        kb = [
            [types.KeyboardButton(text="Предстоящие события на: неделю"), types.KeyboardButton(text="Предстоящие события на: месяц")]
        ]

        keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
        await state.set_state(BOT_STATE.auth)
        await message.answer(f"Успешная авторизация, {message.from_user.first_name} \N{smiling face with smiling eyes}!", reply_markup=keyboard)

    else:
        await message.reply("Некорректные данные, повторите ввод: ")


@router.message(
    BOT_STATE.auth,
    F.text.lower() == 'предстоящие события на: неделю'
)
async def get_events(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    print(user_data)
    if('user_id' in user_data):
        data = await send_events_request('week')
        if (data != 'error'):
            for event in data:
                date_object = datetime.fromisoformat(event['datetime'].rstrip("Z"))
                text = (f"<b>{event['title']}</b>\n"
                        f"{event['description']} \n\n"
                        f"<b>Место</b>: {event['place_title']}\n"
                        f"<b>Время</b>: {date_object}")
                image = URLInputFile(
                    event['cover_uri'],
                    headers={'Authorization': f'Bearer {TOKEN}'}
                )

                await bot.send_photo(message.chat.id, photo=image, caption=text, parse_mode="HTML")


@router.message(
    BOT_STATE.auth,
    F.text.lower() == 'предстоящие события на: месяц'
)
async def get_events(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if('user_id' in user_data):
        data = await send_events_request('month')
        if (data != 'error'):
            for event in data:
                date_object = datetime.fromisoformat(event['datetime'].rstrip("Z"))
                text = (f"<b>{event['title']}</b>\n"
                        f"{event['description']} \n\n"
                        f"<b>Место</b>: {event['place_title']}\n"
                        f"<b>Время</b>: {date_object}")
                image = URLInputFile(
                    event['cover_uri'],
                    headers={'Authorization': f'Bearer {TOKEN}'}
                )

                await bot.send_photo(message.chat.id, photo=image, caption=text, parse_mode="HTML")


@router.message(
    StateFilter(None),
    F.text.lower() == 'предстоящие события'
)
async def get_events_no_auth(message: types.Message, state: FSMContext):
    await state.clear()
    message.answer("Нажмите /start")



async def send_auth_request(email, password, tg_id):
    data = {"telegram_id": tg_id, "email": email, "password": password}
    response = requests.post(BASE_URL + '/users/tg/link', data=json.dumps(data), headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return 'error'



async def send_events_request(type):

    link = ''
    if type == 'week':
        link = '/events/tg?range=week'
    else:
        link = '/events/tg?range=month'

    response = requests.get(BASE_URL + link, headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {TOKEN}'})
    print(response)
    if response.status_code == 200:
        data = response.json()
        print(data)
        filtered_objects = []
        for item in data:
            obj = {
                'id': item['id'],
                'title': item['title'],
                'description': item['description'],
                'cover_uri': BASE_URL + item['cover']['uri'],  # Предполагается структура объекта cover
                'place_title': item['place']['title'],  # Предполагается структура объекта place
                'datetime': item['datetime']
            }
            filtered_objects.append(obj)
        print(filtered_objects)
        return filtered_objects
    else:
        print(response.text)
        return 'error'

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
