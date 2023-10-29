import colorama
from aiohttp   import ClientSession
from .prettify import req_prettify  as rp

async def botinfo(headers: dict):
    async with ClientSession(headers=headers) as session:
        url      = "https://discord.com/api/v9/users/@me"
        response = await session.get(url)
        pr       = rp(response.status, url)
        
        if pr == True:
            return await response.json()
        elif pr == False:
            json = await response.json()
            await asyncio.sleep(json["retry_after"])
            await botinfo(headers)
        else: return False;
					