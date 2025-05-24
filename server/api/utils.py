from database.db import MySqlDb
from io import BytesIO
import database.db_utils as db
from webscraper.danbooru import search_and_get_link_tags

import requests
import json
import os

def get_messages():
    pass

def query_discord(channel_id:str, last_message:str):
    http = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    auth = {"Authorization" : os.environ['DISCORD_AUTH_TOKEN']}

    r = requests.get(http, headers=auth)
    r.raise_for_status()
    
    messages = json.loads(r.text)

    data = []
    for message in messages:
        if message['content'] == last_message:
            break
        metadata = {}
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

            danbooru_link, tags = search_and_get_link_tags(embedding['link'])

            if danbooru_link:
                embedding['danbooru'] = danbooru_link
            if tags:
                embedding['tags'] = tags

            embeddings.append(embedding)
        
        post['embedding'] = embeddings
        if embeddings:
            metadata['has_embed'] = True

        post['metadata'] = metadata
        data.append(post)

    return data

    


