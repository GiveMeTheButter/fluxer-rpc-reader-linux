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
import globalVars

def setStatusNull():
    asyncio.run(patch.setStatusString())

def respondHandshake(connection):
    payload = {
                    "cmd": "DISPATCH",
                    "data": {
                        "v": 1,
                        "config": {
                            "cdn_host": "cdn.discordapp.com",
                            "api_endpoint": "//discord.com/api",
                            "environment": "production"
                        },
                        "user": {
                            "id": "IDDD", 
                            "username": "USER", 
                            "discriminator": "0",
                            "global_name": "XX", 
                            "avatar": "XX", 
                            "avatar_decoration_data": None,
                            "bot": False,
                            "flags": 288,
                            "premium_type": 0
                        }
                    },
                    "evt": "READY",
                    "code": "4000",
                    "nonce": None
                }
    payload = json.dumps(payload).encode("UTF-8")
    payload = struct.pack("<ii", 1, len(payload)) + payload
    connection.send(payload)

def startListening(ipcPath, tray):
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

    globalVars.savedStatus = {"custom_status":""}
    globalVars.savedStatus["custom_status"] = asyncio.run(patch.getStatus())
    if globalVars.savedStatus != None:
        asyncio.run(patch.setStatus(globalVars.savedStatus))
    else:
        asyncio.run(patch.setStatusString())

    conn, addr = soc.accept()
    cid = None

    lastJson = None

    print("Connected with " + str(conn))
    timah = timer.Timer(tray)
    thread = threading.Thread(target=timah.timeLoop)
    thread.daemon = True
    thread.start()
    with conn:
        globalVars.savedStatus = {"custom_status":""}
        globalVars.savedStatus["custom_status"] = asyncio.run(patch.getStatus())
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
            if(lastJson != None):
                jason = {"custom_status":""}
                jason["custom_status"] = asyncio.run(patch.getStatus())
                if(timah.getLastJson() != None):
                    if(timah.getLastJson() != jason):
                        globalVars.savedStatus = {"custom_status":""}
                        globalVars.savedStatus["custom_status"] = asyncio.run(patch.getStatus())
                else:
                    if(lastJson != jason):
                        globalVars.savedStatus = {"custom_status":""}
                        globalVars.savedStatus["custom_status"] = asyncio.run(patch.getStatus())
            asyncio.run(patch.setStatus(processjson.generateStatus(jsonData, cid, timah.getSeconds())))
            lastJson = processjson.generateStatus(jsonData, cid, timah.getSeconds())
            tray.setToolTip(processjson.generateStatus(jsonData, cid, timah.getSeconds(), True))
    if globalVars.savedStatus != None:
        asyncio.run(patch.setStatus(globalVars.savedStatus))
    else:
        asyncio.run(patch.setStatusString())
    tray.setToolTip("Fluxer RPC")
    timah.stop()
    del timah
    print("Disconnected, setting status to null.")
    soc.close()
    startListening(ipcPath,tray)
