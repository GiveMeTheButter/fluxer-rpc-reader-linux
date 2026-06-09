import json
import subprocess

try:
    with open("clientids.json", "r") as file:
        clientids = json.load(file)
except:
    print("Something went wrong when reading clientids.json, does the file exist and is its content correct?")
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

def generateStatus(j:dict, cid:str):
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
                text = '"gaming ' + clientids.get(cid)
            else:
                text = '"gaming ' + str(pidToName(j.get("args").get("pid")))
            emoji_name = '"🎮"'
            if j.get("args").get("activity").get("state") != None:
                text = text + " - " + j.get("args").get("activity").get("state")
            if j.get("args").get("activity").get("details") != None:
                text = text + ", " + j.get("args").get("activity").get("details")
            text = text[:maxTextLength+1]
            text = text + '"'
    print('{"custom_status":{"text":' + text + ',"emoji_name":' + emoji_name + ',"emoji_animated":' + emoji_animated + '}}')
    return json.loads('{"custom_status":{"text":' + text + ',"emoji_name":' + emoji_name + ',"emoji_animated":' + emoji_animated + '}}')