from database.db import MySqlDb
from io import BytesIO
import database.db_utils as db

import requests
import json
import os

def get_messages():
    pass

def query_discord(user_id:str, channel_id:str):
    http = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    auth = {"Authorization" : os.environ['DISCORD_AUTH_TOKEN']}

    r = requests.get(http, headers=auth)
    r.raise_for_status()
    
    messages = json.loads(r.text)

    data = []
    for message in messages:
        post = {
            'time': message['timestamp'],
            'content': message['content'],
        }
        embeddings = []
        for embed in message['embeds']:
            embedding = {
                'link': embed['url'],
                'image': embed['image']['url']
            }
            embeddings.append(embedding)
        data.append(post)


    


