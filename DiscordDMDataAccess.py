import json
import requests

dataFile = ""
sourceID = ""
sourceurl = ""
headers = {"Authorization" : ""}
links = []
targets = []
groups = []
artContent = []

def initialize(file):
    global dataFile
    global sourceID
    global sourceurl
    global headers
    global links
    global targets

    with open(file, 'r') as f:
        data = json.load(f)

    dataFile = file
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

def searchHistory(channelurl):
    global artContent

    r = requests.get(channelurl, headers=headers)
    jsonn = json.loads(r.text)

    for entry in jsonn:
        if entry["content"].startswith(tuple(links)):
            artContent.append(entry["content"])
        else:
            break

def getSourceID():
    global sourceID
    return sourceID

def getSourceUrl():
    global sourceurl
    return sourceurl

def setSource(newID):
    global dataFile
    global sourceID
    global sourceurl

    with open(dataFile, 'r') as f:
        data = json.load(f)
    
    data["source"] = newID
    sourceID = newID
    sourceurl = f"https://discord.com/api/v9/channels/{sourceID}/messages"

    with open(dataFile, 'w') as f:
        json.dump(data, f)

def getHeader():
    global headers
    return headers

def setHeaders(auth):
    global headers

    with open(dataFile, 'r') as f:
        data = json.load(f)
    
    data["Authorization"] = auth
    headers = {"Authorization" : auth}

    with open(dataFile, 'w') as f:
        json.dump(data, f)

def getLinks():
    global links
    return links

def addLink(newLink):
    global links

    with open(dataFile, 'r') as f:
        data = json.load(f)
    
    data["linkTypes"].append(newLink)
    links.append(newLink)

    with open(dataFile, 'w') as f:
        json.dump(data, f)

def removeLink(remLink):
    global links

    with open(dataFile, 'r') as f:
        data = json.load(f)
    
    data["linkTypes"].remove(remLink)
    links.remove(remLink)

    with open(dataFile, 'w') as f:
        json.dump(data, f) 

def getTargets():
    global targets
    return targets

def addTarget(newTarget):
    global targets

    with open(dataFile, 'r') as f:
        data = json.load(f)
    
    data["targets"].append(newTarget)
    targets.append(newTarget)

    with open(dataFile, 'w') as f:
        json.dump(data, f)

def removeTarget(remTarget):
    global targets

    with open(dataFile, 'r') as f:
        data = json.load(f)
    
    data["targets"].remove(remTarget)
    targets.remove(remTarget)

    with open(dataFile, 'w') as f:
        json.dump(data, f)

def getGroups():
    global groups
    return groups

def addGroup(newGroup):
    global groups

    with open(dataFile, 'r') as f:
        data = json.load(f)
    
    data["groups"].append(newGroup)
    groups.append(newGroup)

    with open(dataFile, 'w') as f:
        json.dump(data, f)

def addGroupMember(group, newMember):
    global groups

    with open(dataFile, 'r') as f:
        data = json.load(f)
    
    for entry in data["groups"]:
        if group in entry:
            entry[group].append(newMember)
            groups[group].append(newMember)
            break

    with open(dataFile, 'w') as f:
        json.dump(data, f)

def removeGroup(remMember):
    global groups

    with open(dataFile, 'r') as f:
        data = json.load(f)
    
    data["groups"].remove(remMember)
    groups.remove(remMember)

    with open(dataFile, 'w') as f:
        json.dump(data, f)

def removeGroupMember(group, remMember):
    global groups

    with open(dataFile, 'r') as f:
        data = json.load(f)
    
    for entry in data["groups"]:
        if group in entry:
            entry[group].remove(remMember)
            groups[group].remove(remMember)
            break

    with open(dataFile, 'w') as f:
        json.dump(data, f)

def getContent():
    global artContent
    return artContent

def addContent(newContent):
    global artContent
    artContent.append(newContent)

def removeContent(remContent):
    global artContent
    artContent.remove(remContent)