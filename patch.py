import aiohttp
import json
import re

file = open("token.txt", "r")
token = re.sub(r'[\r\n\x00]', '', str(file.read()))

async def setStatus(j:dict):
    async with aiohttp.ClientSession("https://api.fluxer.app/v1/", headers={"Authorization": token}) as session:
        async with session.patch("/users/@me/settings", json=j) as response:
            html = await response.text()
            if json.loads(html).get("code") == "UNAUTHORIZED":
                print('Fluxer API responding with code "UNAUTHORIZED", is your token correct?')
            await session.close()

async def test(text, emoji):
    j = json.loads('{"custom_status":{"text":' + text + ',"emoji_name":' + emoji + ',"emoji_animated":false}}')
    async with aiohttp.ClientSession("https://api.fluxer.app/v1/", headers={"Authorization": token}) as session:
        async with session.patch("/users/@me/settings", json=j) as response:
            html = await response.text()
            #print(html)
            await session.close()
