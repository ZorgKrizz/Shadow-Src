import asyncio
import aiohttp
from .prettify import req_prettify as rp

async def delete_channel(headers, channel, limiter):
    async with limiter:
        async with aiohttp.ClientSession(headers=headers) as session:
            url = f"https://discord.com/api/v9/channels/{channel}"
            request = await session.delete(url, ssl=False)
    
            response = rp(request.status, url)
            if response == False:
                json = await request.json() 
                await asyncio.sleep(json["retry_after"])
                await delete_channel(headers, channel, limiter)
