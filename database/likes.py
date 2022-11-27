import sqlite3
import sqlite3 as sl

users = ['id', 'admin', 'login', 'password', 'avatar']
post = ['id', 'author_id', 'text', 'image', 'date', 'like', 'dislike']
rates = ['post_id', 'history_id']
history = ['id', 'post_id', 'user_id', 'action']

DB_root = ['users', 'post', 'rates', 'history']
DB = [users, post, rates, history]

#0 = no action
#1 = like
#2 = dislike

def give_last_action(post_id, user_id):
    DB = sl.connect('memes.db')
    hist = []
    with DB:
        data = DB.execute('SELECT history_id FROM rates WHERE post_id == ' + str(post_id))
        for row in data:
            hist = row[0]    
    with DB:
        if hist:
            hist = hist.split(',')
            for i in hist:        
                data1 = DB.execute( 'SELECT action FROM history WHERE id == ' + str(i) + ' and user_id == ' + str(user_id))
                for row in data1:
                    break
                if row[0] >= 0:
                    break
            if row[0]:
                return row[0]
            else:
                return 0
        else:
            return 0


def counter_like(post_id, user_id, last_action, now_action): #counter like or dislike
    DB = sl.connect('memes.db')
    sql = DB.execute('SELECT * FROM post WHERE id == ' + str(post_id))
    for row in sql:
        buf = row
    sql_delete_query = 'DELETE from post where id = ' + str(post_id)
    DB.execute(sql_delete_query)
    if last_action == 1:
        if now_action == 1:
            sql = 'INSERT INTO post(id, author_id, text, image, date, like, dislike) values(?,?,?,?,?,?,?)'
            data = [
                (buf[0], buf[1], buf[2], buf[3], buf[4], buf[5]-1, buf[6]) #loading data, several at once
                ]
            with DB:
                DB.executemany(sql,data)
        elif now_action == 2:
            sql = 'INSERT INTO post(id, author_id, text, image, date, like, dislike) values(?,?,?,?,?,?,?)'
            data = [
                (buf[0], buf[1], buf[2], buf[3], buf[4], buf[5]-1, buf[6]+1) #loading data, several at once
                ]
            with DB:
                DB.executemany(sql,data)
    elif last_action == 2:
        if now_action == 1:
            sql = 'INSERT INTO post(id, author_id, text, image, date, like, dislike) values(?,?,?,?,?,?,?)'
            data = [
                (buf[0], buf[1], buf[2], buf[3], buf[4], buf[5]+1, buf[6]-1) #loading data, several at once
                ]
            with DB:
                DB.executemany(sql,data)
        elif now_action == 2:
            sql = 'INSERT INTO post(id, author_id, text, image, date, like, dislike) values(?,?,?,?,?,?,?)'
            data = [
                (buf[0], buf[1], buf[2], buf[3], buf[4], buf[5], buf[6]-1) #loading data, several at once
                ]
            with DB:
                DB.executemany(sql,data)
    else:
        sql = DB.execute('SELECT * FROM post WHERE id == ' + str(post_id))
        for row in sql:
            buf = row
        sql_delete_query = 'DELETE from post where id = ' + str(post_id)
        DB.execute(sql_delete_query)
        if now_action == 1:
            sql = 'INSERT INTO post(id, author_id, text, image, date, like, dislike) values(?,?,?,?,?,?,?)'
            data = [
                (buf[0], buf[1], buf[2], buf[3], buf[4], buf[5]+1, buf[6]) #loading data, several at once
                ]
            with DB:
                DB.executemany(sql,data)
        elif now_action == 2:
            sql = 'INSERT INTO post(id, author_id, text, image, date, like, dislike) values(?,?,?,?,?,?,?)'
            data = [
                (buf[0], buf[1], buf[2], buf[3], buf[4], buf[5], buf[6]+1) #loading data, several at once
                ]
            with DB:
                DB.executemany(sql,data)


def import_rates(post_id, history_id):
    DB = sl.connect('memes.db')
    info = DB.execute('SELECT * FROM rates WHERE post_id=?', (post_id, ))

    sql = 'INSERT INTO rates(post_id, history_id) values(?,?)'

    if info.fetchone() is None:
        data = [
        (post_id, str(history_id)) #loading data, several at once
        ]
        with DB:
            DB.executemany(sql,data)

    else:
        with DB:
            data1 = DB.execute('SELECT * FROM rates WHERE post_id == '+str(post_id))
            for row in data1:
                buf = row[1]
                
            buf =str(history_id) + ',' + buf
            sql_delete_query = 'DELETE from rates where post_id = ' + str(post_id)
            DB.execute(sql_delete_query)
            
            data = [
            (post_id, buf) #loading data, several at once
            ]
            with DB:
                DB.executemany(sql,data)


def import_history(history_id, post_id, user_id, action):
    DB = sl.connect('memes.db') #path to db
    last_action = give_last_action(post_id, user_id)
    sql = 'INSERT INTO history(id, post_id, user_id, action) values(?,?,?,?)'
    if action == last_action:
        data = [
            (history_id, post_id, user_id, 0) #loading data, several at once
            ]    
        with DB:
            DB.executemany(sql,data)
    else:
        data = [
            (history_id, post_id, user_id, action) #loading data, several at once
            ]    
        with DB:
            DB.executemany(sql,data)
    import_rates(post_id, history_id)
    now_action = action
    counter_like(post_id, user_id, last_action, now_action)


