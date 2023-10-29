import asyncio

from aiohttp import ClientSession
from .prettify import req_prettify as rp

async def ban_member(limiter, headers, guild, member):
    async with limiter:
        async with ClientSession(headers=headers) as session:
            url = f"https://discord.com/api/v9/guilds/{guild}/bans/{member}"
            request = await session.put(url, ssl=False)
            
            response = rp(request.status, url)
            if response == False:
                json = await request.json() 
                await asyncio.sleep(json["retry_after"])
                await ban_member(limiter, headers, guild, member)

        