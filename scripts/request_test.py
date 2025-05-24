import html.parser
import requests
import dotenv
import json
import html
import os
from bs4 import BeautifulSoup

dotenv.load_dotenv('server/.env')

def searchHistory():
    http = f"https://discord.com/api/v9/channels/{os.environ['SOURCE_CHANNEL_ID']}/messages"
    auth = {"Authorization" : os.environ['DISCORD_AUTH_TOKEN']}
    r = requests.get(http, headers=auth)
    jsonn = json.loads(r.text)
    jsonn = jsonn[0]
    print(json.dumps(jsonn, indent=4))

def searchImage():
    http = f"https://pbs.twimg.com/media/GrjjwfcagAAeMip.jpg:large"
    image = requests.get(http)
    print(image.content)

def sendMsg(payload):
    http = f"https://discord.com/api/v9/channels/{os.environ['DEST_CHANNEL_ID']}/messages"
    auth = {
        "Authorization" : os.environ['DISCORD_AUTH_TOKEN']
    }
    res = requests.post(http, json=payload, headers=auth)
    print(f"Status Code: {res.status_code}")

def getHtml():
    http = f"https://danbooru.donmai.us/posts?tags=source%3Ahttps%3A%2F%2Ftwitter.com%2Fpalizyok%2Fstatus%2F1904168220363272638"
    r = requests.get(http)  

    soup = BeautifulSoup(r.text, 'html.parser')

    target_div = soup.find('a', class_='post-preview-link')

    if target_div:
        # print(f"Found div by class:\n{target_div.prettify()}")
        print(target_div.get("href"))

searchHistory()