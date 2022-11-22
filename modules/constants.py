USERS_TABLENAME = 'users'
POSTS_TABLENAME = 'post'
RATES_TABLENAME = 'rates'
HISTORY_TABLENAME = 'history'

USED_TABLES = [USERS_TABLENAME, POSTS_TABLENAME, RATES_TABLENAME, HISTORY_TABLENAME]

USER_FIELDNAMES = ('id', 'admin', 'login',  'password', 'avatar', 'email')
POST_FIELDNAMES = ('id', 'author_id', 'text', 'image', 'date', 'like', 'dislike')
RATES_FIELDNAMES = ('id', 'history_id')
HISTORY_FIELDNAMES = ('id', 'post_id', 'user_id', 'action')

ADMIN_STATE = 1
USER_STATE = 0

USERS_INDIVIDUAL_FIELDS = [True, False, True, False, False, True]


USERS_TABLE_GENERATOR_SQL = '''
    create table users (
        id integer primary key autoincrement not null,
        admin integer not null,
        login text not null,
        password text not null,
        avatar text not null,
        email text not null 
         )'''


POSTS_TABLE_GENERATOR_SQL = '''
    create table post (
        id integer primary key autoincrement not null,
        author_id integer not null,
        text text not null,
        image text not null,
        date text not null,
        like integer not null,
        dislike integer not null 
        ) '''

RATES_TABLE_GENERATOR_SQL = '''
        create table rates (
            post_id integer primary key autoincrement not null,
            history_id integer not null
        )
        
        '''

HISTORY_TABLE_GENERATOR_SQL = '''
        create table history (
            id integer primary key autoincrement not null,
            post_id integer not null,
            user_id integer not null,
            action integer not null 
        )
'''

FIELDS_CONTAINER = {
    USERS_TABLENAME: USER_FIELDNAMES,
    POSTS_TABLENAME: POST_FIELDNAMES,
    RATES_TABLENAME: RATES_FIELDNAMES,
    HISTORY_TABLENAME: HISTORY_FIELDNAMES
}

SQL_GENERATORS_CONTAINERS = {
    USERS_TABLENAME: USERS_TABLE_GENERATOR_SQL,
    POSTS_TABLENAME: POSTS_TABLE_GENERATOR_SQL,
    RATES_TABLENAME: RATES_TABLE_GENERATOR_SQL,
    HISTORY_TABLENAME: HISTORY_TABLE_GENERATOR_SQL
}
