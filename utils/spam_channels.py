import asyncio

from aiohttp import ClientSession
from .prettify import req_prettify as rp

async def spam_channels(limiter, headers, guild, name):
    async with limiter:
        async with ClientSession(headers=headers) as session:
            url     = f"https://discord.com/api/v9/guilds/{guild}/channels"
            payload = {"name": name, "type":0}
            request = await session.post(url, json=payload, ssl=False)
            
            response = rp(request.status, url)
            if response == False:
                json = await request.json() 
                await asyncio.sleep(json["retry_after"])
                await spam_channels(limiter, headers, guild, name)