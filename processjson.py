import json
import subprocess
import os
import sys
from pathlib import Path

rootDir = os.path.dirname(sys.argv[0])
clientidPath = Path(os.path.join(rootDir,"clientids.json"))

if clientidPath.exists() != True:
    print("clientids.json doesn't exist! Created clientids.json for you :)")
    clientidFile = open(clientidPath, "w")
    clientidFile.write("{\n\n}")
    clientidFile.close()

try:
    with open(clientidPath, "r") as file:
        clientids = json.load(file)
except:
    print("Something went wrong when reading clientids.json, does the file exist and is its content correct?")
    clientids = json.loads("{ }")
maxTextLength = 128

def pidToName(pid):
    command = subprocess.Popen(["ps", "-p", str(pid), "-o", "comm="], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, _ = command.communicate()
    return stdout.strip()

def identifyJson(json):
    a = 0
    f = 1
    found = False
    z = 0
    for x in json:
        if found == False:
            if x == "{":
                found = True
                z = a + 1
            else:
                a = a + 1
        else:
            if x == "}":
                f = f - 1
            if x == "{":
                f = f + 1
            z = z + 1
            if f == 0:
                jsone = json[a:]
                jsone = jsone[:z]
                return jsone

def generateStatus(j:dict, cid:str, seconds, needText:bool=False):
    seconds = seconds
    text = ""
    emoji_name = ""
    emoji_animated = "false"
    if j.get("cmd") == None or j.get("cmd") != "SET_ACTIVITY":
        return None

    if j.get("args" == None):
        text = "null"
        emoji_name = "null"
    else:
        if j.get("args").get("activity") == None:
            text = "null"
            emoji_name = "null"
        else:
            if cid != None and clientids.get(cid) != None:
                text = 'gaming ' + clientids.get(cid)
            else:
                text = 'gaming ' + str(pidToName(j.get("args").get("pid")))
            emoji_name = '🎮'
            if j.get("args").get("activity").get("state") != None:
                text = text + " - " + j.get("args").get("activity").get("state")
            if j.get("args").get("activity").get("details") != None:
                text = text + ", " + j.get("args").get("activity").get("details")
            if seconds != None:
                m,s = divmod(seconds,60)
                if len(str(s)) == 1:
                    s = "0"+str(s)
                time = f"{m}:{s}"
                text = text[:maxTextLength-len(time)]
                text = text + " " + time
            text = text[:maxTextLength]
    jsone = json.loads('{"custom_status":{"text":"","emoji_name":null,"emoji_animated":' + emoji_animated + '}}')
    jsone.get("custom_status")["text"] = text
    jsone.get("custom_status")["emoji_name"] = emoji_name
    jsone.get("custom_status")["emoji_animated"] = emoji_animated
    print("Clientid: "+ str(cid))
    print(jsone)
    if(needText==False):
        return jsone
    else:
        return text