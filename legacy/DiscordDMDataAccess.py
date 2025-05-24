# Json Accessor for Discord DM
# by David Zhou
# version 1.5
import json
import requests
from random import randint
from re import split

class DiscordDMAccessor:
    dataFile = ""
    sourceID = ""
    sourceurl = ""
    headers = {"Authorization" : ""}
    links = []
    targets = []
    groups = {}
    messages = []

    def __init__(self, file):
        self.dataFile = ""
        self.sourceID = ""
        self.sourceurl = ""
        self.headers = {"Authorization" : ""}
        self.links = []
        self.targets = []
        self.groups = {}
        self.messages = []
        try:
            with open(file, 'r') as f:
                data = json.load(f)
        except Exception:
            data = open(file, 'w')
            jsonn = {
                "source": "",
                "Authorization": "",
                "linkTypes": [],
                "targets": [],
                "groups": []
            }
            data.write(json.dumps(jsonn))
            data.close()

        self.dataFile = file
        self.sourceID = data["source"]
        self.auth = data["Authorization"]
        self.sourceurl = f"https://discord.com/api/v9/channels/{self.sourceID}"
        self.headers = {"Authorization" : self.auth}
        for link in data["linkTypes"]:
            self.links.append(link)
        for target in data["targets"]:
            self.targets.append(target)
        self.groups = data["groups"]
        self.searchHistory(self.sourceurl)

    def searchHistory(self, channelurl):
        r = requests.get(channelurl, headers=self.headers)
        jsonn = json.loads(r.text)
        try:
            for entry in jsonn:
                if entry["content"].startswith(tuple(self.links)):
                    self.messages.append({"link" : split("\s+", entry["content"])[0],
                                    "sendGroup" : split("\s+", entry["content"])[1],
                                    "other" : entry})
                else:
                    break
        except Exception:
            return
        
        self.messages.reverse()

    def getSourceID(self):
        return self.sourceID

    def getSourceUrl(self):
        return self.sourceurl

    def setSource(self, newID):
        with open(self.dataFile, 'r') as f:
            data = json.load(f)
        
        data["source"] = newID
        self.sourceID = newID
        self.sourceurl = f"https://discord.com/api/v9/channels/{self.sourceID}/messages"

        with open(self.dataFile, 'w') as f:
            json.dump(data, f)

    def getHeader(self):
        seed = ""
        offset = 0
        encoded = self.headers["Authorization"]
        for i in range(11):
            seed += encoded[offset]
            encoded = encoded[:offset] + encoded[offset+1:]
            offset += int(seed[i])
        string = ""
        for char in str(seed):
            match char:
                case "0":
                    string += "P"
                case "1":
                    string += "K"
                case "2":
                    string += "G"
                case "3":
                    string += "X"
                case "4":
                    string += "U"
                case "5":
                    string += "C"
                case "6":
                    string += "L"
                case "7":
                    string += "W"
                case "8":
                    string += "Z"
                case "9":
                    string += "M"
        seed = str(seed)
        cur = 0
        dejunked = ""
        for char in encoded:
            if char == string[cur]:
                cur = (cur + 1) % 10
                dejunked += "|"
                continue
            dejunked += char if char.isnumeric() else ""
        letters = dejunked.split("|")
        auth = ""
        for letter in letters:
            if letter != "":
                auth += chr(int(int(letter) / int(seed) + .5))
        return auth

    def setHeaders(self, auth):
        encoded = ""
        seed = randint(10000000000, 99999999999)
        string = ""
        for char in str(seed):
            match char:
                case "0":
                    string += "P"
                case "1":
                    string += "K"
                case "2":
                    string += "G"
                case "3":
                    string += "X"
                case "4":
                    string += "U"
                case "5":
                    string += "C"
                case "6":
                    string += "L"
                case "7":
                    string += "W"
                case "8":
                    string += "Z"
                case "9":
                    string += "M"
        for i, char in enumerate(auth):
            encoded += str(ord(char) * seed)
            encoded += string[i % 10]
        offset = 0
        cur = 0
        junkEncode = ""
        for char in encoded:
            if not char.isnumeric():
                cur = (cur + 1) % 10
            if randint(0,1):
                val = randint(33, 116)
                if val > 47:
                    val += 10
                junkEncode += chr(val) if chr(val) != string[cur] else ""
            junkEncode += char
        seed = str(seed)
        encoded = junkEncode
        for char in seed:
            encoded  = encoded[:offset] + char + encoded[offset:]
            offset += int(char) + 1

        with open(self.dataFile, 'r') as f:
            data = json.load(f)
        
        data["Authorization"] = encoded
        self.headers = {"Authorization" : encoded}

        with open(self.dataFile, 'w') as f:
            json.dump(data, f)

    def getLinks(self):
        return self.links

    def addLink(self, newLink):
        with open(self.dataFile, 'r') as f:
            data = json.load(f)
        
        data["linkTypes"].append(newLink)
        self.links.append(newLink)

        with open(self.dataFile, 'w') as f:
            json.dump(data, f)

    def removeLink(self, remLink):
        with open(self.dataFile, 'r') as f:
            data = json.load(f)
        
        data["linkTypes"].remove(remLink)
        self.links.remove(remLink)

        with open(self.dataFile, 'w') as f:
            json.dump(data, f) 

    def getTargets(self):
        return self.targets

    def addTarget(self, newTarget):
        with open(self.dataFile, 'r') as f:
            data = json.load(f)
        
        data["targets"].append(newTarget)
        self.targets.append(newTarget)

        with open(self.dataFile, 'w') as f:
            json.dump(data, f)

    def removeTarget(self, remTarget):
        with open(self.dataFile, 'r') as f:
            data = json.load(f)
        
        data["targets"].remove(remTarget)
        self.targets.remove(remTarget)

        with open(self.dataFile, 'w') as f:
            json.dump(data, f)

    def getGroups(self):
        return self.groups

    def addGroup(self, newGroup):
        with open(self.dataFile, 'r') as f:
            data = json.load(f)
        
        data["groups"][newGroup] = []
        self.groups[newGroup] = []

        with open(self.dataFile, 'w') as f:
            json.dump(data, f)

    def addGroupMember(self, group, newMember):
        with open(self.dataFile, 'r') as f:
            data = json.load(f)
        
        data["groups"][group].append(newMember)
        self.groups[group].append(newMember)

        with open(self.dataFile, 'w') as f:
            json.dump(data, f)

    def removeGroup(self, remGroup):
        global groups

        with open(self.dataFile, 'r') as f:
            data = json.load(f)
        
        data["groups"].pop(remGroup)
        self.groups.pop(remGroup)

        with open(self.dataFile, 'w') as f:
            json.dump(data, f)

    def removeGroupMember(self, group, remMember):
        global groups

        with open(self.dataFile, 'r') as f:
            data = json.load(f)
        
        data["groups"][group].remove(remMember)
        self.groups[group].remove(remMember)

        with open(self.dataFile, 'w') as f:
            json.dump(data, f)

    def getContent(self):
        return self.messages

    def addContent(self, newContent):
        self.messages.append(newContent)

    def removeContent(self, remContent):
        self.messages.remove(remContent)