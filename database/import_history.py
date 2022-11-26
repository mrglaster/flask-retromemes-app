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

history_id = 6
post_id = 5
user_id = 6
action = 2

def import_history(history_id, post_id, user_id, action):
    con = sl.connect('memes.db') #path to db
    sql = 'INSERT INTO history(id, post_id, user_id, action) values(?,?,?,?)'
    data = [
        (history_id, post_id, user_id, action) #loading data, several at once
        ]
    with con:
        con.executemany(sql,data)


    
   
import_history(history_id, post_id, user_id, action)
