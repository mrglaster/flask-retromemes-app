import sqlite3
import sqlite3 as sl
from modules.users import User
from modules.posts import Post
from modules.rates import Rates
from dataclasses import astuple
from modules.constants import *


def get_rowcount(connection, tablename):
    """Gets amount of rows in the table."""
    try:
        cursor = connection.cursor()
        cursor.execute(f"select * from {tablename}")
        results = cursor.fetchall()
        return len(results)
    except:
        raise ValueError(f"Error occured during getting data from table {tablename}. Check if tablename is valid")


def get_newestId(connection, tablename):
    """gets id can be used for adding data"""
    return get_rowcount(connection, tablename) + 1


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    # try:
    conn = sl.connect(db_file)
    # except Error as e:
    #     print(e)
    return conn


def _dataclass_to_strtuple(dataclass_element):
    """converts dataclass object to string-like tuple"""
    return _process_tuple(astuple(dataclass_element))


def _process_tuple(working_tuple):
    """processes tuple as string"""
    if len(working_tuple) == 0:
        return '()'
    result_string = '('
    for i in working_tuple:
        result_string += "'" + i + "', "
    return result_string[:-2] + ')'


def delete_row_bId(connection, table_name, row, idname='id'):
    """Deletes row in some table by row's id"""
    sql_request = f'DELETE FROM {table_name} WHERE id={row}'
    cur = connection.cursor()
    cur.execute(sql_request)
    """
    temp_table_name = f'temp_{table_name}_{idname}'
    connection.execute(f'create temp table {temp_table_name} as select * from {table_name} order by id')
    connection.execute(f'drop table {table_name}')
    connection.execute(modules.constants.SQL_GENERATORS_CONTAINERS[table_name])
    connection.execute(f'insert into {table_name}   select * from {temp_table_name} order by {idname}')
    connection.execute(f'drop table {temp_table_name}')
    """
    connection.commit()


def clear_table(connection, table_name):
    """Clears the whole table!"""
    sql_request = f'DELETE FROM {table_name}'
    cur = connection.cursor()
    cur.execute(sql_request)
    connection.commit()


def _generate_adding_sqlrequest(tablename, table_field_names):
    """Generates SQL Request adding data to SQL table"""
    return f"INSERT INTO {tablename}{_process_tuple(table_field_names)} values{'(' + ('?, ' * len(table_field_names))[:-2] + ')'}".replace("'", '')


def get_table_column(connection, table_name, column_name):
    """Returns all values from column of some table"""
    cursor = connection.cursor()
    cursor.execute(f"SELECT {column_name} FROM {table_name}")
    return cursor.fetchall()


def is_value_used(connection, table_name, column_name, value):
    """Checks if input value was already used in some column"""
    all_columns = get_table_column(connection, table_name, column_name)
    for i in all_columns:
        column_value = str(i).replace('(', '').replace(')', '').replace("'", '').replace(',', '')
        if column_value == value:
            return True
    return False


def add_data(connection, tablename, dataclass_element, individual_fields=None):
    """Appends data to table.
    @:param connection: sqlite.connection object
    @:param tablename: name of the table to which we'll put the data
    @:param dataclass_element: data class object which we'll put into the table
    @:param individual_field : array of booleans, containing information about,
    that data in some field must be individual and may not be repeated in the table (for E-mails, logins etc).
    Example: [True, False, True]
    """
    field_names = FIELDS_CONTAINER[tablename]
    if individual_fields is not None and len(individual_fields) != len(field_names):
        raise ValueError(
            f"Amounts of elements in individual_fields and field_names don't concide: {len(individual_fields)} and {len(field_names)}")
    sql_request = _generate_adding_sqlrequest(tablename, field_names)
    latest_id = get_newestId(tablename=tablename, connection=connection)
    dataclass_element.id = latest_id
    data_tuple = astuple(dataclass_element)
    if individual_fields is not None:
        for i in range(len(individual_fields)):
            used = is_value_used(connection=connection, table_name=tablename, column_name=field_names[i],
                                 value=data_tuple[i])
            if individual_fields[i] and used:
                print(f"Such data was already used: {field_names[i]} =  {data_tuple[i]}")
                return 100
    with connection:
        connection.executemany(sql_request, [data_tuple])
        connection.commit()
    return 200


def _process_table_rowdata(table_name, data):
    """Processes table row as object of dataclass"""
    if table_name == 'users':
        a, f, b, c, d, e = data
        return User(a, f, b, c, d, e)
    if table_name == 'post':
        a, b, c, d, e, f, g = data
        return Post(a, b, c, d, e, f, g)
    if table_name == 'rates':
        a, b, c = data
        return Rates(a, b, c)
    raise ValueError(f"Unknown table name: {table_name}")


def get_all_tabledata(connection, table_name, result_as_dataclass=False):
    """Gets all data from the table"""
    with connection:
        data = connection.execute(f'SELECT * FROM {table_name}')
    if not result_as_dataclass:
        return data
    dataclass_result = []
    for i in data:
        dataclass_result.append(_process_table_rowdata(table_name, i))
    return dataclass_result


def array_toDataclass(array, table_name):
    """Transforms bunch of table rows to concisting dataclasses"""
    if len(array) == 0:
        raise ValueError("Expected array with length > 0 ")
    result = []
    for i in array:
        print(table_name)
        result.append(_process_table_rowdata(table_name, i))
    return result


def get_latest_rows(connection, table_name, rows_amount, result_as_dataclass=False):
    """Returns latesn n rows of a table"""
    if rows_amount <= 0:
        raise ValueError("Wrong requested posts amount: expeced positive number")
    data = connection.cursor().execute(f"SELECT * FROM ( SELECT * FROM {table_name} ORDER BY id DESC LIMIT {rows_amount})").fetchall()
    if not result_as_dataclass:
        return data
    return array_toDataclass(data, table_name)


def create_database(db_file):
    """Creates tables for our project's database and writes them to db file"""
    connection = create_connection(db_file)
    connection.execute(USERS_TABLE_GENERATOR_SQL)
    connection.execute(POSTS_TABLE_GENERATOR_SQL)
    connection.execute(RATES_TABLE_GENERATOR_SQL)
    connection.commit()
    

def print_table(connection, table_name):
    """Prints a SQLite table"""
    try:
        with connection:
            data = connection.execute(f'SELECT * FROM {table_name}')
            for row in data:
                print(row)
                print('----------')
    except:
        raise ValueError(f"Requested table {table_name} doesn't exist!")

        
def drop_db(connection):
    """Clears all data from database."""
    for i in USED_TABLES:
        clear_table(connection, i)
    connection.commit()



def get_userid_byname(user_name, db_file):
    """Gets user's id by it's username"""
    connection = create_connection(db_file)
    sql_querry = f"SELECT id FROM users WHERE login='{user_name}'"
    result = connection.execute(sql_querry).fetchall()[0][0]
    connection.close()
    return result    
    
    
def delete_post_bID(post_id, connection, basic_path):
    """Delete post by it's id"""
    try:
        sql_request = f"SELECT image from post where id='{post_id}'"
        result = connection.execute(sql_request).fetchall()[0][0]
        if len(result) == 0:
            return 100
        print(f"Removing path: {basic_path+'//'+result}")
        os.remove(basic_path+'\\'+result)
        delete_row_bId(connection, 'post', post_id)
        return 200
    except:
        return 100
    
def is_user_admin(connection, user_data, user_data_type='id'):
    """Checks if user with input id or login is an admin"""
    if user_data_type == 'id' or user_data_type == 'login':
        sql_request = f"SELECT admin from users where {user_data_type}='{user_data}'"
        result = connection.execute(sql_request).fetchall()[0][0]
        print(f"Checking user with name = {user_data} and result = {result}", file=sys.stdout)
        return result == ADMIN_STATE
    raise ValueError(f'Unable user data type: {user_data_type}, value = {user_data}')


def add_admin(db_file, admin_name):
    """Creates new synthetic administrator user with name = admin_name"""
    connection = create_connection(db_file)
    add_data(connection=connection, tablename='users',
             dataclass_element=User(1, 1, admin_name, 'root', DEFAULT_AVATAR, 'nope'),
             individual_fields=USERS_INDIVIDUAL_FIELDS)
    connection.commit()
