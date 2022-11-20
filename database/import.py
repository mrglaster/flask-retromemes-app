import sqlite3
import sqlite3 as sl

users = ['id', 'login', 'password', 'avatar']
post = ['id', 'author_id', 'text', 'image', 'date', 'like', 'dislike']
rates = ['post_id', 'real_likes', 'real_dislikes']

DB_root = ['users', 'post', 'rates']
DB = [users, post, rates]

con = sl.connect('memes.db') #path to db
sql = 'INSERT INTO users(id, login, password, avatar) values(?,?,?,?)'
data = [
    (1, 'GogaGGPlay', 'qwerty', '/memes.org') #loading data, several at once
    ]
with con:
    con.executemany(sql,data)
