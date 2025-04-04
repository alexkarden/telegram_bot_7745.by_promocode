import sqlite3


async def create_db():
    conn = sqlite3.connect('base.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id integer auto_increment primary key, tgid integer, first_name text, last_name text, username text, useradd integer, userblock integer, usersubs integer)')
    conn.commit()
    cur.close()
    conn.close()


async def add_user_db(tgid, first_name, last_name,username, useradd, userblock, usersubs):
    conn = sqlite3.connect('base.db')
    cur = conn.cursor()
    info = cur.execute('SELECT * FROM users WHERE tgid=?', (tgid,)).fetchone()
    if info is None:
        cur.execute("INSERT INTO users (tgid, first_name, last_name,username, useradd, userblock, usersubs) VALUES ('%s', '%s','%s','%s','%s', '%s','%s')" % (tgid, first_name, last_name,username,useradd, userblock, usersubs))
        conn.commit()
        return False
    else:
        return True
    cur.close()
    conn.close()



async def user_subs_db(tgid):
    conn = sqlite3.connect('base.db')
    cur = conn.cursor()
    info = cur.execute('SELECT * FROM users WHERE tgid=?', (tgid,)).fetchone()
    if info is None:
        return False
    else:
        cur.execute('UPDATE users  SET usersubs = 1 WHERE tgid=?', (tgid,))
        conn.commit()
        return True
    cur.close()
    conn.close()

async def user_unsubs_db(tgid):
    conn = sqlite3.connect('base.db')
    cur = conn.cursor()
    info = cur.execute('SELECT * FROM users WHERE tgid=?', (tgid,)).fetchone()
    if info is None:
        return False
    else:
        cur.execute('UPDATE users  SET usersubs = 0 WHERE tgid=?', (tgid,))
        conn.commit()
        return True
    cur.close()
    conn.close()


async def get_status_used_db(tgid):
    conn = sqlite3.connect('base.db')
    cur = conn.cursor()
    info = cur.execute('SELECT * FROM users WHERE tgid=? AND usersubs = 1', (tgid,)).fetchone()
    if info is None:
        y = '🔔 Включить уведомления'
        return y
    else:
        y = '🔕 Выключить уведомления'
        return y
    cur.close()
    conn.close()


async def get_user_list_db():
    conn = sqlite3.connect('base.db')
    cur = conn.cursor()
    info = cur.execute('SELECT * FROM users WHERE usersubs=1').fetchall()
    list =[]
    for el in info:
        list.append(el[1])
    cur.close()
    conn.close()
    return list


