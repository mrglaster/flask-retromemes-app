import sqlite3
import sqlite3 as sl
from modules.constants import *
from modules.database import *


def give_last_action(post_id, user_id):
    """Returns latest usre's action for post"""
    DB = sl.connect(DATABASE_PATH)
    hist = []
    with DB:
        data = DB.execute('SELECT history_id FROM rates WHERE post_id == ' + str(post_id))
        for row in data:
            hist = row[0]
    with DB:
        if hist:
            hist = hist.split(',')
            for i in hist:
                data1 = DB.execute(
                    'SELECT action FROM history WHERE id == ' + str(i) + ' and user_id == ' + str(user_id))
                for row in data1:
                    break
                if len(str(row[0])) >= 0:
                    break
            if row[0]:
                return row[0]
            else:
                return 0
        else:
            return 0


def counter_like(post_id, user_id, last_action, now_action):  
    """Conter for likes/dislikes"""
    DB = sl.connect(DATABASE_PATH)
    sql = DB.execute('SELECT * FROM post WHERE id == ' + str(post_id))
    for row in sql:
        buf = row
    sql_delete_query = 'DELETE from post where id = ' + str(post_id)
    DB.execute(sql_delete_query)
    if last_action == 1:
        if now_action == 1:
            sql = 'INSERT INTO post(id, author_id, text, image, date, like, dislike) values(?,?,?,?,?,?,?)'
            data = [
                (buf[0], buf[1], buf[2], buf[3], buf[4], buf[5] - 1, buf[6])  # loading data, several at once
            ]
            with DB:
                DB.executemany(sql, data)
        elif now_action == 2:
            sql = 'INSERT INTO post(id, author_id, text, image, date, like, dislike) values(?,?,?,?,?,?,?)'
            data = [
                (buf[0], buf[1], buf[2], buf[3], buf[4], buf[5] - 1, buf[6] + 1)  # loading data, several at once
            ]
            with DB:
                DB.executemany(sql, data)
    elif last_action == 2:
        if now_action == 1:
            sql = 'INSERT INTO post(id, author_id, text, image, date, like, dislike) values(?,?,?,?,?,?,?)'
            data = [
                (buf[0], buf[1], buf[2], buf[3], buf[4], buf[5] + 1, buf[6] - 1)  # loading data, several at once
            ]
            with DB:
                DB.executemany(sql, data)
        elif now_action == 2:
            sql = 'INSERT INTO post(id, author_id, text, image, date, like, dislike) values(?,?,?,?,?,?,?)'
            data = [
                (buf[0], buf[1], buf[2], buf[3], buf[4], buf[5], buf[6] - 1)  # loading data, several at once
            ]
            with DB:
                DB.executemany(sql, data)
    else:
        sql = DB.execute('SELECT * FROM post WHERE id == ' + str(post_id))
        for row in sql:
            buf = row
        sql_delete_query = 'DELETE from post where id = ' + str(post_id)
        DB.execute(sql_delete_query)
        if now_action == 1:
            sql = 'INSERT INTO post(id, author_id, text, image, date, like, dislike) values(?,?,?,?,?,?,?)'
            data = [
                (buf[0], buf[1], buf[2], buf[3], buf[4], buf[5] + 1, buf[6])  # loading data, several at once
            ]
            with DB:
                DB.executemany(sql, data)
        elif now_action == 2:
            sql = 'INSERT INTO post(id, author_id, text, image, date, like, dislike) values(?,?,?,?,?,?,?)'
            data = [
                (buf[0], buf[1], buf[2], buf[3], buf[4], buf[5], buf[6] + 1)  # loading data, several at once
            ]
            with DB:
                DB.executemany(sql, data)


def import_rates(post_id, history_id):
    """Rates import"""
    DB = sl.connect(DATABASE_PATH)
    info = DB.execute('SELECT * FROM rates WHERE post_id=?', (post_id,))

    sql = 'INSERT INTO rates(post_id, history_id) values(?,?)'

    if info.fetchone() is None:
        data = [
            (post_id, str(history_id))  # loading data, several at once
        ]
        with DB:
            DB.executemany(sql, data)

    else:
        with DB:
            data1 = DB.execute('SELECT * FROM rates WHERE post_id == ' + str(post_id))
            for row in data1:
                buf = row[1]

            buf = str(history_id) + ',' + buf
            sql_delete_query = 'DELETE from rates where post_id = ' + str(post_id)
            DB.execute(sql_delete_query)

            data = [
                (post_id, buf)  # loading data, several at once
            ]
            with DB:
                DB.executemany(sql, data)


def import_history(post_id, user_id, action):
    """History import"""
    DB = sl.connect(DATABASE_PATH)  # path to db
    last_action = give_last_action(post_id, user_id)
    history_id = get_newestId(create_connection(DATABASE_PATH), 'history')
    sql = 'INSERT INTO history(id, post_id, user_id, action) values(?,?,?,?)'
    if action == last_action:
        data = [
            (history_id, post_id, user_id, 0)  # loading data, several at once
        ]
        with DB:
            DB.executemany(sql, data)
    else:
        data = [
            (history_id, post_id, user_id, action)  # loading data, several at once
        ]
        with DB:
            DB.executemany(sql, data)
    import_rates(post_id, history_id)
    now_action = action
    counter_like(post_id, user_id, last_action, now_action)