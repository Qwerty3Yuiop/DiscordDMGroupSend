import requests
import json
import re
import time

# potential future implementation for automated classification of images
# from openai import OpenAI

# Discord art scanner and sender
# by David Zhou
# version 1.0

sourceurl = ""
headers = {"Authorization" : ""}
payload = {"content" : ""}
links = []
targets = []
groups = []
artContent = []


def parseContent(file):
    f = open(file)
    data = json.load(f)
    global sourceurl
    global headers
    sourceID = data["source"]
    auth = data["Authorization"]
    sourceurl = f"https://discord.com/api/v9/channels/{sourceID}/messages"
    headers = {"Authorization" : auth}
    for link in data["linkTypes"]:
        links.append(link)
    for target in data["targets"]:
        targets.append(target)
    for group in data["groups"]:
        groups.append(group)
    f.close()

def retrieveMsg(channelurl):
    r = requests.get(channelurl, headers=headers)
    jsonn = json.loads(r.text)
    return jsonn

def searchContent(file):
    for entry in file:
        if entry["content"].startswith(tuple(links)):
            artContent.append(entry["content"])
        else:
            break

#def parseArt():
#    for item in artContent:
#        r = requests.get(item)
#        html = r.text
#        print(html)

def bulkMsg(group, art, skip):
    print("\n\n", art, "\n")
    print("Messages will be sent to these users:\n")
    targetsInGroup = []
    targetsInGroup.clear()
    for user in group:
        print(user["name"])
        targetsInGroup.append(user)
    print("Type the number of the person you want to add or remove:\n")
    count = 0
    for user in targets:
        print(f"{count}: ", user["name"])
        count += 1
    userIn = -1
    while skip:
        userIn = int(input("input a number[]: "))
        if userIn < 0 or userIn > 20:
            break
        alter = {}
        for user in targets:
            if userIn == 0:
                alter = user
                break
            userIn -= 1
        print(alter)
        removed = False
        for user in targetsInGroup:
            if(user == alter):
                targetsInGroup.remove(alter)
                removed = True
                break
        if not removed:
            targetsInGroup.append(alter)
    
    payload = {"content" : re.split("\s+", art)[0]}
    for user in targetsInGroup:
        print(user)
    for user in targetsInGroup:
        sendMsg(user["id"], payload)

def identify(str):
    code = re.split("\s+", str)
    symb = code[1].strip().lower()
    group = ""
    match symb:
        case "gm":
            group = "genshinmale"
        case "gf":
            group = "genshinfemale"
        case "gh":
            group = "genshinhorny"
        case "ak":
            group = "arknights"
        case "sr":
            group = "starrail"
        case "oc":
            group = "originalchar"
        case "ot":
            group = "other"
    return group

def sendMsg(channelID, payload):
    time.sleep(.200)
    res = requests.post(f"https://discord.com/api/v9/channels/{channelID}/messages", payload, headers=headers)


def main():
    #f = open("OpenAIKey.txt")
    #client = OpenAI(api_key = f.readline(),)
    #f.close()
    #chat_completion = client.chat.completions.create(
    #    messages=[
    #        {
    #            "role": "user",
    #            "content": "Respond with the hashtags of the following link in a comma seperated list: ###https://vxtwitter.com/qiandaiyiyu/status/1768970513278226560###",
    #        }
    #    ],
    #    model="gpt-3.5-turbo",
    #)
    #print(chat_completion.choices[0].message.content)
    userin = input("will you make exceptions for this send?[y/n]\n")
    if userin.lower() == "y":
        skip = True
    else:
        skip = False
    parseContent("data/DiscordDM_DATA.json")
    msgList = retrieveMsg(sourceurl)
    searchContent(msgList)
    for art in artContent:
        artGroup = identify(art)
        for group in groups:
            try:
                bulkMsg(group[artGroup], art, skip)
            except Exception:
                pass


main()
