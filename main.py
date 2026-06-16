import socket
import os
import json
import struct
import patch
import asyncio
import subprocess
import processjson
import sys
import timer
import threading
# add other paths later!!!

if sys.platform == "win32":
    raise ValueError("Windows is not currently supported")
ipcPath = str(os.environ.get("XDG_RUNTIME_DIR")) + "/" + "discord-ipc-0"
print("Path: " + ipcPath)

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
        try:
            print("Trying to remove and recreate " + str(ipcPath))
            os.remove(ipcPath)
            soc.bind((ipcPath))
        except:   
            print("Failed to bind. Code: "
            + str(message.errno) + ", Msg: "
            + message.strerror
            )

    soc.listen()
    asyncio.run(patch.test('null','null'))

    conn, addr = soc.accept()
    cid = None

    print("Connected with " + str(conn))
    timah = timer.Timer()
    thread = threading.Thread(target=timah.timeLoop)
    thread.daemon = True
    thread.start()
    with conn:
        while True:
            data = conn.recv(2048)
            if not data:
                break
            decodedData = data.decode("Latin-1")
            decodedData = processjson.identifyJson(decodedData)
            decodedData = decodedData.encode("Latin-1")
            try:
                decodedData = decodedData.decode("UTF-8")
            except UnicodeDecodeError:
                print("Couldn't decode this string: " + str(decodedData))
                break
            try:
                jsonData = json.loads(decodedData)
            except json.JSONDecodeError as e:
                break
            if jsonData.get("v") != None and jsonData.get("client_id") != None:
                cid = jsonData.get("client_id")
                respondHandshake(conn)
            if jsonData.get("args") != None:
                if jsonData.get("args").get("activity") != None:
                    timah.setCurrentJsonAndCid(jsonData,cid)
            asyncio.run(patch.setStatus(processjson.generateStatus(jsonData, cid, timah.getSeconds())))
    asyncio.run(patch.test('null','null'))
    timah.stop()
    del timah
    print("Disconnected, setting status to null.")
    soc.close()
try:
    while True:
        startListening()
except KeyboardInterrupt:
    print("KeyboardInterrupt catched, setting custom status to null.")
    asyncio.run(patch.test('null','null'))
