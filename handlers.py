from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboards import create_main_keyboard, create_dynamic_keyboard
import time
from scripts import convert_date_to_str
from scripts_db import add_user_db, subscribed_user_db, unsubscribed_user_db, get_promokod_db, set_old_promokod_db, get_time_of_add_user_db, get_old_promokod_db





router = Router()
@router.message(CommandStart())
async def cmd_start(message: Message):
    curent_time = int(time.time())
    await message.answer('👋 <b> Добро пожаловать! </b> \n  Бот по запросу ищет промокоды 7745:', reply_markup = create_main_keyboard(), parse_mode=ParseMode.HTML)
    await add_user_db(message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username)
    for kod in await get_promokod_db(curent_time):
        await message.answer(f'Промокод: <b>{kod[1]}</b> действует до {convert_date_to_str(kod[2])} на <a href="{kod[3]}">{kod[4]}</a> - {kod[5]}',reply_markup= create_main_keyboard(),  parse_mode='html')


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Это команда /help')

@router.message(Command('about'))
async def cmd_about(message: Message):
    await message.answer('<b>Alex Karden</b>\nhttps://github.com/alexkarden', reply_markup= create_main_keyboard(), parse_mode=ParseMode.HTML)

@router.message(Command('alexkarden'))
async def cmd_alexkarden(message: Message):
    await message.answer('<b>Алексей\n<a href="tel:+375297047262">+375-29-704-72-62</a></b>', parse_mode=ParseMode.HTML)


@router.message()
async def all_message(message: Message):
    text = message.text
    curent_time = int(time.time())
    if text == '🛒 Получить промокоды 7745':
        for kod in  await get_promokod_db(curent_time):
            await message.answer(f'Промокод: <b>{kod[1]}</b> действует до {convert_date_to_str(kod[2])} на <a href="{kod[3]}">{kod[4]}</a> - {kod[5]}',reply_markup= create_main_keyboard(),  parse_mode='html')
    elif text == '⚙️ Настройки':
        await message.answer('Здесь Вы можете включить/выключить уведомления',reply_markup=await create_dynamic_keyboard(message.from_user.id),  parse_mode='html')
    elif text == '🔙 Выйти из настроек':
        await message.reply(f'<b>Настройки сохранены!</b>',reply_markup= create_main_keyboard(), parse_mode='html')
    elif text == '🔔 Подписаться':
        await subscribed_user_db(message.from_user.id)
        await message.reply(f'<b>Уведомления включены!</b>', reply_markup=await create_dynamic_keyboard(message.from_user.id), parse_mode='html')
    elif text == '🔕 Отписаться':
        await unsubscribed_user_db(message.from_user.id)
        await message.reply(f'<b>Уведомления выключены!</b>', reply_markup=await create_dynamic_keyboard(message.from_user.id), parse_mode='html')
    elif text == 'alexkarden':
        await message.answer('<b>Алексей\n<a href="tel:+375297047262">+375-29-704-72-62</a></b>', parse_mode='html')
    elif text == 'История Ваших промокодов':
        x = 'История ваших промокодов:\n'
        for kod in await get_old_promokod_db(await get_time_of_add_user_db(message.from_user.id)):

            if kod == 0:
                x = 'Пока нет промокодов'


            else:

                x += f'Промокод: <b>{kod[1]}</b> действует до {convert_date_to_str(kod[2])} на <a href="{kod[3]}">{kod[4]}</a> - {kod[5]}\n'


        await message.answer( f'{x}', reply_markup=create_main_keyboard(), parse_mode='html')


    else:
        await message.answer('Воспользуйтесь клавиатурой ниже:', parse_mode='html')
