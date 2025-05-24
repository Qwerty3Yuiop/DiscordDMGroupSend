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

@router.post("/messages/get")
async def retrieve_messages(msg: EncryptedRequest):
    conn = db.get_db()
    public_key, private_key = db.get_keys(conn, msg.user_id)
    request:Request = crypt.rsa_decrypt(msg.body, private_key)

