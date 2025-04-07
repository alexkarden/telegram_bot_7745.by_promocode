import aiosqlite
import logging
import time
from config import DATABASE_NAME
from scripts import convert_date




# Инициализация базы данных
async def init_db():
    try:
        async with aiosqlite.connect(DATABASE_NAME) as db:
            # Создание таблицы users, если она еще не существует
            await db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_id INTEGER UNIQUE, first_name TEXT, last_name TEXT, username TEXT, user_added INTEGER NOT NULL, user_subscribed INTEGER NOT NULL, user_blocked INTEGER NOT NULL, time_of_add INTEGER)")
            # Создание таблицы promokods, если она еще не существует
            await db.execute("CREATE TABLE IF NOT EXISTS promokods (id INTEGER PRIMARY KEY, promokod TEXT, expiration_date INTEGER , link TEXT, link_caption TEXT, description TEXT, time_of_add INTEGER, new_promokod INTEGER)")
            await db.commit()
    except aiosqlite.Error as e:
        print(f"Ошибка при инициализации базы данных: {e}")

# Добавление пользователя в базу данных
async def add_user_db(user_id, first_name, last_name, username):
    time_of_add = int(time.time())
    try:
        async with aiosqlite.connect(DATABASE_NAME) as db:
            # Проверка, существует ли пользователь в базе данных
            async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()
                if result is not None:
                    # Если пользователь существует, можно обновить его данные
                    await db.execute("UPDATE users SET first_name = ?, last_name = ?, username = ?, user_added = ? WHERE user_id = ? ", (first_name, last_name, username, 1, user_id))
                    print(f"Пользователь с ID {user_id} обновлен в базе данных.")
                else:
                    # Если не существует, добавляем нового пользователя
                    await db.execute("INSERT INTO users (user_id, first_name, last_name, username, user_added, user_subscribed, user_blocked, time_of_add) VALUES (?, ?, ?, ?, ?, ?, ?,?)", (user_id, first_name, last_name, username, 1, 0, 0,time_of_add))
                    print(f"Пользователь с ID {user_id} добавлен в базу данных.")
                await db.commit()
    except aiosqlite.Error as e:
        print(f"Ошибка при добавлении пользователя в базу данных: {e}")

# Обработка подписки
async def subscribed_user_db(user_id):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute("UPDATE users SET user_subscribed = 1 WHERE user_id = ?", (user_id,))
        await db.commit()

# Обработка отписки
async def unsubscribed_user_db(user_id):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        await db.execute("UPDATE users SET user_subscribed = 0 WHERE user_id = ?", (user_id,))
        await db.commit()

#Получение статуса подписки
async def get_status_subscribed_user_db(user_id):
    try:
        async with aiosqlite.connect(DATABASE_NAME) as db:
            async with db.execute("SELECT user_subscribed FROM users WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()
                if result is None:
                    # Если пользователь не найден, можно вернуть None или выбросить исключение
                    return None  # Пользователь не найден
                return result[0]  # Возвращаем статус подписки (True/False)
    except aiosqlite.Error as e:
        # Обработка ошибок базы данных
        print(f"Ошибка доступа к базе данных: {e}")
        return None  # В случае ошибки также можем вернуть None


#Получение времени регистрации пользователя
async def get_time_of_add_user_db(user_id):
    try:
        async with aiosqlite.connect(DATABASE_NAME) as db:
            async with db.execute("SELECT time_of_add FROM users WHERE user_id = ?", (user_id,)) as cursor:
                result = await cursor.fetchone()
                if result:
                    print(result)
                    return result  # Возвращаем время
    except aiosqlite.Error as e:
        # Обработка ошибок базы данных
        print(f"Ошибка доступа к базе данных: {e}")
        return None  # В случае ошибки также можем вернуть None

# Получение списка пользователей для рассылки
async def get_list_subscribed_user_db():
    try:
        async with aiosqlite.connect(DATABASE_NAME) as db:
            async with db.execute("SELECT user_id FROM users WHERE user_subscribed = 1") as cursor:
                list = await cursor.fetchall()  # Здесь должен быть await для получения результата
                user_ids = [user[0] for user in list]
                return user_ids
    except aiosqlite.Error as e:
        # Логируем ошибку или обрабатываем её как-то иначе
        print(f"Произошла ошибка при получении списка пользователей: {e}")
        return []  # Возвращаем пустой список в случае ошибки



# Добавление промокода в базу данных
async def add_promokod_db(promokod, strexpiration_date, link, link_caption, description, time_of_add):
    expiration_date = convert_date(strexpiration_date)
    # Проверка, только среди тех прококодов которые актуальны
    async with aiosqlite.connect(DATABASE_NAME) as db:
        async with db.execute("SELECT * FROM promokods WHERE promokod =? AND expiration_date=?", (promokod, expiration_date,)) as cursor:
            result = await cursor.fetchone()
            if result is not None:
                # Если промокод существует, можно обновить его данные
                logging.info(f"Промокод '{promokod}' уже существует и будет обновлен.")
                await db.execute("UPDATE promokods SET link = ?, link_caption = ?, description = ? WHERE promokod = ? AND expiration_date = ?",(link, link_caption, description, promokod, expiration_date))
                await db.commit()
            else:
                # Если не существует, добавляем новыйпромокод
                await db.execute("INSERT INTO promokods (promokod, expiration_date, link, link_caption, description, time_of_add, new_promokod) VALUES (?, ?, ?, ?, ?, ?, ?)",(promokod, expiration_date, link, link_caption, description, time_of_add, 1))
                await db.commit()


# Извлечение актуальных промокодов
async def get_promokod_db(curent_time):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        async with db.execute("SELECT * FROM promokods WHERE expiration_date >=?", (curent_time,)) as cursor:
            result = await cursor.fetchall()
            if result is not None:
                # Если промокоды существуют, возвращаем
                return result
            else:
                # Если не существует,
                return []


# смена статуса промокода
async def set_old_promokod_db():
    async with aiosqlite.connect(DATABASE_NAME) as db:
        async with db.execute("SELECT * FROM promokods WHERE new_promokod =?", (1,)) as cursor:
            result = await cursor.fetchall()
            if result:
                # Если промокоды существуют, возвращаем
                await db.execute("UPDATE promokods SET new_promokod = ? WHERE new_promokod = ?", (0, 1))
                await db.commit()


# Извлечение промокодов появившехся позже регистрации пользователя
async def set_old_promokod_db(time):
    async with aiosqlite.connect(DATABASE_NAME) as db:
        async with db.execute("SELECT * FROM promokods WHERE time_of_add >=?", (time)) as cursor:
            result = await cursor.fetchall()
            if result:
                return result
