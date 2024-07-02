import requests
from time import sleep
# Discord message sender
# by David Zhou
# version 1.0


class Messenger:
    headers = {"Authorization" : ""}
    def __init__(self, auth):
        self.headers = auth

    def bulkMsg(self, groups, arts):
        for art in arts:
            try:
                payload = {"content" : art["link"]}
                print(self.headers)
                for user in groups[art["sendGroup"].lower()]:
                    response = self.sendMsg(user["id"], payload)

                    if response == "<Response [429]>":
                        sleep(5)
                        response = self.sendMsg(user["id"], payload)
            except Exception:
                print("skip")
                continue
            sleep(3)
        return -1


    def sendMsg(self, channelID, payload):
        res = requests.post(f"https://discord.com/api/v9/channels/{channelID}/messages", payload, headers=self.headers)
        #print(res)
        return res.__str__() # == "<Response [429]>"
