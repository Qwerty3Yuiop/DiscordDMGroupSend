from db import MySqlDb
import auth.encrypt as crypt
from datetime import datetime
import uuid

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

def save_message(db:MySqlDb, time:str, message:str, embedding:str, metadata:str, user_id:str):
    """
    Saves a new message to the database
    """
    msg_id = str(uuid.uuid4())
    time = datetime.strptime(time, TIMEFORMAT)
    message_blob = crypt.fernet_encrypt(message)
    embedding_blob = crypt.fernet_encrypt(embedding)
    metadata_blob = crypt.fernet_encrypt(metadata)

    query = '''INSERT INTO messages (id, time, message, embedding, metadata, user_id)
        VALUES (%s, %s, %s, %s, %s, %s)'''
    
    params = (msg_id, time, message_blob, embedding_blob, metadata_blob, user_id)
    db.query(query, params)
    db.commit()

def get_messages_by_time(db:MySqlDb, start:str, end:str):
    t_start = datetime.strptime(start, TIMEFORMAT)
    t_end = datetime.strptime(end, TIMEFORMAT)

    query = '''SELECT * FROM messages WHERE time >= %s AND time <= %s'''
    params = (t_start, t_end)

    data = db.query(query, params)
    return data
