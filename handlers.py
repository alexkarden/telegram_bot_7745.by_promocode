from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from keyboards import main_kb, dinamic_kb
from scripts import get_kod
from scripts_db import create_db, add_user_db, user_subs_db, user_unsubs_db, get_user_list_db






router = Router()
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('👋 <b> Добро пожаловать! </b> \n  Бот по запросу ищет промокоды 7745:', reply_markup=main_kb, parse_mode=ParseMode.HTML)
    await add_user_db(message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                      message.from_user.username,1,0,0)


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Это команда /help')

@router.message(Command('about'))
async def cmd_about(message: Message):
    await message.answer('<b>Alex Karden</b>\nhttps://github.com/alexkarden', reply_markup=main_kb, parse_mode=ParseMode.HTML)

@router.message(Command('alexkarden'))
async def cmd_alexkarden(message: Message):
    await message.answer('<b>Алексей\n<a href="tel:+375297047262">+375-29-704-72-62</a></b>', parse_mode=ParseMode.HTML)


@router.message()
async def all_message(message: Message):
    text = message.text
    if text == '🛒 Получить промокоды 7745':
        for kod in  await get_kod():
            await message.answer(f'Промокод: <b>{kod[1]}</b> действует до {kod[0]} на <a href="{kod[2]}">{kod[3]}</a> - {kod[4]}',reply_markup=main_kb,  parse_mode='html')
    elif text == '⚙️ Настройки':
        await message.answer('Здесь Вы можете включить/выключить уведомления',reply_markup=await dinamic_kb(message.from_user.id),  parse_mode='html')
    elif text == '🔙 Выйти из настроек':
        await message.reply(f'<b>Настройки сохранены!</b>',reply_markup=main_kb, parse_mode='html')
    elif text == '🔔 Включить уведомления':
        await user_subs_db(message.from_user.id)
        await message.reply(f'<b>Уведомления включены!</b>', reply_markup=await dinamic_kb(message.from_user.id), parse_mode='html')
    elif text == '🔕 Выключить уведомления':
        await user_unsubs_db(message.from_user.id)
        await message.reply(f'<b>Уведомления выключены!</b>', reply_markup=await dinamic_kb(message.from_user.id), parse_mode='html')
    elif text == 'alexkarden':
        await message.answer('<b>Алексей\n<a href="tel:+375297047262">+375-29-704-72-62</a></b>', parse_mode='html')
    else:
        await message.answer('Воспользуйтесь клавиатурой ниже:', parse_mode='html')
