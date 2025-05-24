import auth.encrypt as crypt
import database.db_utils as db

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

import utils

router = FastAPI()

class EncryptedRequest(BaseModel):
    user_id: str
    body: bytes

class Request(BaseModel):
    type: str
    content: str

class ChannelRequest(BaseModel):
    channel: str

@router.post("/messages/check")
async def check_messages(msg: EncryptedRequest):
    conn = db.get_db()
    public_key, private_key = db.get_keys(conn, msg.user_id)
    request:ChannelRequest = crypt.rsa_decrypt(msg.body, private_key)

    last_message = db.get_messages_recent(conn, msg.user_id)
    data = utils.query_discord(request.channel, last_message[0]['message'])

