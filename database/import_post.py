import sqlite3
import sqlite3 as sl

users = ['id', 'admin', 'login', 'password', 'avatar']
post = ['id', 'author_id', 'text', 'image', 'date', 'like', 'dislike']
rates = ['post_id', 'history_id']
history = ['id', 'post_id', 'user_id', 'action']

DB_root = ['users', 'post', 'rates', 'history']
DB = [users, post, rates, history]

#1 = like
#2 = dislike
 #path to db

post_id = 5
history_id = 6
def import_rates(post_id, history_id):
    con = sl.connect('memes.db')
    info = con.execute('SELECT * FROM rates WHERE post_id=?', (post_id, ))

    sql = 'INSERT INTO rates(post_id, history_id) values(?,?)'

    if info.fetchone() is None:
        data = [
        (post_id, str(history_id)) #loading data, several at once
        ]
        with con:
            con.executemany(sql,data)

    else:
        with con:
            data1 = con.execute('SELECT * FROM rates WHERE post_id == '+str(post_id))
            for row in data1:
                buf = row[1]
                
            buf =str(history_id) + ',' + buf
            sql_delete_query = 'DELETE from rates where post_id = ' + str(post_id)
            con.execute(sql_delete_query)
            
            data = [
            (post_id, buf) #loading data, several at once
            ]
            with con:
                con.executemany(sql,data)

import_rates(post_id, history_id)
