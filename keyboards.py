from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from scripts_db import get_status_used_db

async def dinamic_kb(tgid):
    y = await get_status_used_db(tgid)
    main_dinamic_kb= ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=y)],
        [KeyboardButton(text='🔙 Выйти из настроек')]
    ], resize_keyboard=True)
    return main_dinamic_kb



main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='🛒 Получить промокоды 7745')],
    [KeyboardButton(text='⚙️ Настройки')]
], resize_keyboard=True)

