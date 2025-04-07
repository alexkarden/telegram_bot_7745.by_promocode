import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import TOKEN, CHECKINTERVAL
from handlers import router
from scripts_db import init_db,  add_promokod_db
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apsсhed import check_promo,check_and_add_promo
from scripts import get_kod
import time

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    curent_time = int(time.time())
    await init_db()
    for kod in await get_kod():
        await  add_promokod_db(kod[1], kod[0], kod[2], kod[3], kod[4],curent_time)
    scheduler = AsyncIOScheduler(timezone="Europe/Minsk")
    scheduler.add_job(check_promo, trigger='interval', minutes=CHECKINTERVAL,
                       kwargs={'bot': bot})
    scheduler.add_job(check_and_add_promo, trigger='interval', minutes=CHECKINTERVAL)

    scheduler.start()
    dp.include_router(router)
    await dp.start_polling(bot)




if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='py_log.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.debug("A DEBUG Message")
    logging.info("An INFO")
    logging.warning("A WARNING")
    logging.error("An ERROR")
    logging.critical("A message of CRITICAL severity")


    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')