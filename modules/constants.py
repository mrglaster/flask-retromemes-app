USERS_TABLENAME = 'users'
POSTS_TABLENAME = 'post'
RATES_TABLENAME = 'rates'

USED_TABLES = [USERS_TABLENAME, POSTS_TABLENAME, RATES_TABLENAME]

USER_FIELDNAMES = ('id', 'admin', 'login',  'password', 'avatar', 'email')
POST_FIELDNAMES = ('id', 'author_id', 'text', 'image', 'date', 'like', 'dislike')
RATES_FIELDNAMES = ('id', 'real_likes', 'real_dislikes')

USERS_TABLE_GENERATOR_SQL = '''
    create table IF NOT EXISTS  users (
        id integer primary key autoincrement not null,
        admin integer not null,
        login text not null,
        password text not null,
        avatar text not null,
        email text not null 
         )'''


POSTS_TABLE_GENERATOR_SQL = '''
    create table IF NOT EXISTS  post (
        id integer primary key autoincrement not null,
        author_id integer not null,
        text text not null,
        image text not null,
        date text not null,
        like integer not null,
        dislike integer not null 
        ) '''

RATES_TABLE_GENERATOR_SQL = '''
        create table IF NOT EXISTS rates (
            post_id integer primary key autoincrement not null,
            real_likes text not null
            real_dislikes text not null )
        
        '''

FIELDS_CONTAINER = {
    USERS_TABLENAME: USER_FIELDNAMES,
    POSTS_TABLENAME: POST_FIELDNAMES,
    RATES_TABLENAME: RATES_FIELDNAMES
}

SQL_GENERATORS_CONTAINERS = {
    USERS_TABLENAME: USERS_TABLE_GENERATOR_SQL,
    POSTS_TABLENAME: POSTS_TABLE_GENERATOR_SQL,
    RATES_TABLENAME: RATES_TABLE_GENERATOR_SQL
}
