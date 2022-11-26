import sqlite3
import sqlite3 as sl

users = ['id', 'login', 'password', 'avatar']
post = ['id', 'author_id', 'text', 'image', 'date', 'like', 'dislike']
rates = ['post_id', 'history_id']

DB_root = ['users', 'post', 'rates']
DB = [users, post, rates]

user_id = 6
post_id = 5
def give_action(post_id, user_id):
    con = sl.connect('memes.db')
    hist = []
    with con:
        data = con.execute('SELECT history_id FROM rates WHERE post_id == ' + str(post_id))
        for row in data:
            hist = row[0]
    hist = hist.split(',')
    with con:        
        for i in hist:        
            data1 = con.execute( 'SELECT action FROM history WHERE id == ' + str(i) + ' and user_id == ' + str(user_id))
            for row in data1:
                flag = False
            if row[0]:
                flag = True
                break
    return row[0]
print (give_action(post_id, user_id))

