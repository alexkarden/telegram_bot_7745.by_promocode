from aiogram import Bot
from scripts import get_kod
from scripts_db import get_user_list_db

async def check_promo(bot:Bot):
    x = await get_kod()
    with open('promo.txt', 'r') as file:
        promo = file.read()
    if str(x) == str(promo):
        return True
    else:
        try:
            with open('promo.txt', 'w') as file:
                file.writelines(str(x))
            for i in await get_user_list_db():
                for kod in x:
                    try:
                        await bot.send_message(i,
                                               f'Промокод: <b>{kod[1]}</b> действует до {kod[0]} на <a href="{kod[2]}">{kod[3]}</a> - {kod[4]}',
                                               parse_mode='html')
                        print(f'Отправлено {i}')
                    except:
                        print(F'Не отправлено {i}')
        except:
            return False

