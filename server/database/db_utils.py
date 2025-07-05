from database.db import MySqlDb
import auth.encrypt as crypt
from datetime import datetime
import uuid
import json

TIMEFORMAT = r"%Y-%m-%dT%H:%M:%S.%f%z"

def get_db():
    return MySqlDb()

def get_keys(db:MySqlDb, user_id:str):
    """
    Gets keys from database.
    Private key is used to decrypt user messages.
    Public key is used to encode messages to user.
    """
    query = f'SELECT public_key, private_key FROM users WHERE id="{user_id}"'
    data = db.query(query)
    if len(data):
        encrypt_pub = crypt.fernet_decrypt(data[0]['public_key'].encode())
        encrypt_pri = crypt.fernet_decrypt(data[0]['private_key'].encode())
        pub_key = crypt.str_to_rsa_pub(encrypt_pub)
        pri_key = crypt.str_to_rsa_pri(encrypt_pri)
        return pub_key, pri_key
    else:
        raise LookupError("user not in table")

def get_user_data(db:MySqlDb, user_id:str):
    """
    Gets user data from database.
    Returns a dictionary with user data.
    """
    query = f'SELECT data FROM users WHERE id="{user_id}"'
    data = db.query(query)
    if len(data):
        return data[0]['data']
    else:
        raise LookupError("user not in table")

def save_message(db:MySqlDb, user_id:str, time:str, message:str, embeddings:list, tags:list):
    """
    Saves a new message to the database
    """
    msg_id = str(uuid.uuid4())
    time = datetime.strptime(time, TIMEFORMAT)

    query = '''INSERT INTO messages (id, time, message, embeddings, tags, user_id)
        VALUES (%s, %s, %s, %s, %s, %s)'''
    
    params = (msg_id, time, message, embeddings, tags, user_id)
    db.query(query, params)
    db.commit()

def get_messages_by_time(db:MySqlDb, user_id:str, start:str, end:str):
    if start and end:
        t_start = datetime.strptime(start, TIMEFORMAT)
        t_end = datetime.strptime(end, TIMEFORMAT)
        query = 'SELECT * FROM messages WHERE user_id = %s AND time >= %s AND time <= %s ORDER BY time DESC'
        params = (user_id, t_start, t_end)
        data = db.query(query, params)
    elif start:
        t_start = datetime.strptime(start, TIMEFORMAT)
        query = 'SELECT * FROM messages WHERE user_id = %s AND time >= %s ORDER BY time DESC'
        params = (user_id, t_start)
        data = db.query(query, params)
    elif end:
        t_end = datetime.strptime(end, TIMEFORMAT)
        query = 'SELECT * FROM messages WHERE user_id = %s AND time <= %s ORDER BY time DESC'
        params = (user_id, t_end)
        data = db.query(query, params)
    else:
        query = 'SELECT * FROM messages WHERE user_id = %s ORDER BY time DESC'
        params = (user_id)
        data = db.query(query, params)

    
    return data

def get_messages_recent(db: MySqlDb, user_id:str, count:int=1):
    query = 'SELECT * FROM messages WHERE user_id = %s ORDER BY time DESC LIMIT %s'
    params = (user_id, count)
    data = db.query(query, params)
    return data

def get_messages_unsent(db: MySqlDb, user_id:str, sent:bool):
    query = 'SELECT * FROM messages WHERE user_id = %s AND sent = %s ORDER BY time DESC'
    params = (user_id, sent)
    data = db.query(query, params)
    return data