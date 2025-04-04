import asyncio
import logging
import apsсhed
from aiogram import Bot, Dispatcher
from config import TOKEN, CHECKINTERVAL
from handlers import router
from scripts_db import create_db
from apscheduler.schedulers.asyncio import AsyncIOScheduler

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    print(CHECKINTERVAL)
    await create_db()
    scheduler = AsyncIOScheduler(timezone="Europe/Minsk")
    scheduler.add_job(apsсhed.check_promo, trigger='interval', minutes=CHECKINTERVAL,
                       kwargs={'bot': bot})
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