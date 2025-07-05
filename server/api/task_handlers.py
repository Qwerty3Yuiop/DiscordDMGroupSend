import auth.encrypt as crypt
import database.db_utils as db

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

import json
import api.utils as utils

router = APIRouter(prefix="/api", tags=["task_handlers"])

class EncryptedRequest(BaseModel):
    user_id: str
    body: bytes

class ChannelRequest(BaseModel):
    channel: str
    type: str

@router.post("/messages/check")
async def check_messages(msg: EncryptedRequest):
    conn = db.get_db()
    public_key, private_key = db.get_keys(conn, msg.user_id)
    request:ChannelRequest = json.loads(crypt.rsa_decrypt(msg.body, private_key))

    last_message = db.get_messages_recent(conn, msg.user_id)
    data = utils.query_discord(request.channel, last_message[0]['message'])

    if len(data) > 0:
        for item in data:
            db.save_message(conn, msg.user_id, item['time'], item['message'], item['embeddings'], item['tags'])
    
    if request.type == "ALL":
        data = db.get_messages_by_time(conn, msg.user_id, "", "")
    elif request.type == "UNSENT":
        data = db.get_messages_unsent(conn, msg.user_id, False)
    elif request.type == "SENT":
        data = db.get_messages_unsent(conn, msg.user_id, True)
    
    encrypted_data = crypt.rsa_encrypt(json.dumps(data), public_key)
    return encrypted_data


        

