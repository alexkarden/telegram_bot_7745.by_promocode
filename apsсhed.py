from aiogram import Bot
from scripts import convert_date_to_str, get_kod
from scripts_db import get_list_subscribed_user_db, get_promokod_db,set_old_promokod_db, add_promokod_db
import time

async def check_promo(bot:Bot):
    curent_time = int(time.time())
    for kod in await get_promokod_db(curent_time):
        if kod[7] == 1:
            await set_old_promokod_db()
            print('Новый промокод')
            for i in await get_list_subscribed_user_db():
                    try:
                        await bot.send_message(i,
                                               f'Промокод: <b>{kod[1]}</b> действует до {convert_date_to_str(kod[2])} на <a href="{kod[3]}">{kod[4]}</a> - {kod[5]}',parse_mode='html')
                        print(f'Отправлено {i}')
                    except:
                        print(F'Не отправлено {i}')



async def check_and_add_promo():
    curent_time = int(time.time())
    for kod in await get_kod():
        await  add_promokod_db(kod[1], kod[0], kod[2], kod[3], kod[4], curent_time)
