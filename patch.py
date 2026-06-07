import fluxer
import asyncio
import aiohttp
import json

file = open("token.txt", "r")
token = str(file.read())

j = json.loads('{"custom_status":{"text":"api test 5","emoji_name":"🎮","emoji_animated":false}}')

async def test(text, emoji):
    j = json.loads('{"custom_status":{"text":' + text + ',"emoji_name":' + emoji + ',"emoji_animated":false}}')
    async with aiohttp.ClientSession("https://api.fluxer.app/v1/", headers={"Authorization": token}) as session:
        async with session.patch("/users/@me/settings", json=j) as response:
            html = await response.text()
            #print(html)
            await session.close()
#asyncio.run(test(j))
