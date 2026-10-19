import aiohttp
import json
import re
import sys
import os
import asyncio
from pathlib import Path

rootDir = os.path.dirname(sys.argv[0])
token = Path(os.path.join(rootDir,"token.txt"))

def getToken():
    file = open(token, "r")
    return re.sub(r'[\r\n\x00]', '', str(file.read()))

async def getStatus():
    async with aiohttp.ClientSession("https://api.fluxer.app/v1/", headers={"Authorization": str(getToken())}) as session:
        while (True):
            try:
                async with session.get("/users/@me/settings") as response:
                    jei = json.loads(await response.text())
                    print(str(jei.get("custom_status")))
                    return jei.get("custom_status")
            except aiohttp.client_exceptions.ClientConnectorDNSError:
                print("GET: Cannot connect to Fluxer API, trying again. (Potentially no internet connection?)")
                await asyncio.sleep(5)

async def setStatus(j:dict):
    async with aiohttp.ClientSession("https://api.fluxer.app/v1/", headers={"Authorization": str(getToken())}) as session:
        try:
            async with session.patch("/users/@me/settings", json=j) as response:
                html = await response.text()
                if json.loads(html).get("code") == "UNAUTHORIZED":
                    print('Fluxer API responding with code "UNAUTHORIZED", is your token correct?')
                await session.close()
        except aiohttp.client_exceptions.ClientConnectorDNSError:
            print("Cannot connect to Fluxer API, there might be no internet connection.")

async def setStatusString(text="null", emoji="null"):
    j = json.loads('{"custom_status":{"text":' + text + ',"emoji_name":' + emoji + ',"emoji_animated":false}}')
    async with aiohttp.ClientSession("https://api.fluxer.app/v1/", headers={"Authorization": str(getToken())}) as session:
        try:
            async with session.patch("/users/@me/settings", json=j) as response:
                html = await response.text()
                await session.close()
        except aiohttp.client_exceptions.ClientConnectorDNSError:
            print("Cannot connect to Fluxer API, there might be no internet connection.")
