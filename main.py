import socket
import os
import json
import struct
import patch
import asyncio
import subprocess

ipcPath = str(os.environ.get("XDG_RUNTIME_DIR")) + "/" + "discord-ipc-0"
print("Path: " + ipcPath)

def identifyJson(json):
    a = 0
    f = 1
    found = False
    z = 0
    for x in json:
        #print(str(f) + " " + x)
        
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
                #print(str(len(json)))
                #print("a: "+str(a)+" z: "+str(z))
                jsone = json[a:]
                jsone = jsone[:z]
                return jsone

def respondHandshake(connection):
    payload = {
                    "cmd": "DISPATCH",
                    "evt": "READY",
                    "code": "4000"
                }
    payload = json.dumps(payload).encode("UTF-8")
    payload = struct.pack("<ii", 1, len(payload)) + payload
    connection.send(payload)

def startListening():
    soc = socket.socket(socket.AF_UNIX)

    try:
        if os.path.exists(ipcPath):
            os.unlink(ipcPath)
        soc.bind((ipcPath))

    except socket.error as message:
        print("Failed to bind. Code: "
        + str(message.errno) + ", Msg: "
        + message.strerror
        )

    soc.listen()
    asyncio.run(patch.test('null','null'))

    conn, addr = soc.accept()
    test = 0

    print("Connected with " + str(conn))
    with conn:
        while True:
            data = conn.recv(2048)
            if not data:
                break
            if test == 0:
                respondHandshake(conn)
                test = test + 1
            decodedData = data.decode("Latin-1",errors="replace")
            decodedData = identifyJson(decodedData)
            decodedData = decodedData.encode("Latin-1")
            decodedData = decodedData.decode("UTF-8")
            jsonData = json.loads(decodedData)
            if jsonData.get("cmd") == "SET_ACTIVITY":
                pid = jsonData.get("args").get("pid")
                command = subprocess.Popen(["ps", "-p", str(pid), "-o", "comm="], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, _ = command.communicate()
                name = stdout.strip()
                state = jsonData.get("args").get("activity")
                if state != None:
                    state = state.get("state")
                else:
                    state = "None"
                asyncio.run(patch.test('"gaming ' + name + ' - ' + str(state) + '"','"🎮"'))
                print(name + " - " + str(state))
    asyncio.run(patch.test('null','null'))
    print("Disconnected")
    soc.close()

while True:
    startListening()