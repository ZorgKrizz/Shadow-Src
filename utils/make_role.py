import asyncio

from aiohttp import ClientSession
from .prettify import req_prettify as rp

async def make_role(limiter, headers, guild, name):
    async with limiter:
        async with ClientSession(headers=headers) as session:
            url = f"https://discord.com/api/v9/guilds/{guild.id}/roles"
            payload = {"name": name}
            request = await session.post(url, ssl=False)
            
            response = rp(request.status, url)
            if response == False:
                json = await request.json() 
                await asyncio.sleep(json["retry_after"])
                await make_role(limiter, headers, guild, name)