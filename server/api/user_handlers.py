import auth.encrypt as crypt
import database.db_utils as db

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

import json
import api.utils as utils

router = APIRouter(prefix="/user", tags=["user_handlers"])


class EncryptedRequest(BaseModel):
    user_id: str
    body: bytes

class ChannelRequest(BaseModel):
    channel: str
    type: str

@router.post("/data/get")
def get_user_data(request: EncryptedRequest):
    conn = db.get_db()
    public_key, private_key = db.get_keys(conn, request.user_id)
    
    try:
        user_data = db.get_user_data(conn, request.user_id)
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        
        encrypted_data = crypt.rsa_encrypt(json.dumps(user_data), public_key)
        return {"data": encrypted_data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))