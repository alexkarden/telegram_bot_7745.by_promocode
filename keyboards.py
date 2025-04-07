from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from scripts_db import get_status_subscribed_user_db

async def create_dynamic_keyboard(tgid):
    # Получаем статус подписки пользователя из базы данных
    is_subscribed = await get_status_subscribed_user_db(tgid)
    # Определение текста кнопки на основе статуса подписки
    subscription_button_text = '🔕 Отписаться' if is_subscribed else '🔔 Подписаться'
    # Создание динамической клавиатуры с учетом статуса подписки
    dynamic_keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=subscription_button_text)],
        [KeyboardButton(text='🔙 Выйти из настроек')]
    ], resize_keyboard=True)
    return dynamic_keyboard



def create_main_keyboard():
    #Создание главной клавиатуры.
    main_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='🛒 Получить промокоды 7745')],
            [KeyboardButton(text='История Ваших промокодов')],
            [KeyboardButton(text='⚙️ Настройки')]
        ],
        resize_keyboard=True
    )
    return main_keyboard

