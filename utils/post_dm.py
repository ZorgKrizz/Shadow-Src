import asyncio

from aiohttp import ClientSession
from .prettify import req_prettify as rp

async def post_dm(limiter, headers, channel, message):
    async with limiter:
        async with ClientSession(headers=headers) as session:
            url = f"https://discord.com/api/v9/channels/{channel}/messages"
            payload = {"content": message, "tts": False}
            request = await session.post(url, json=payload, ssl=False)
            
            response = rp(request.status, url)
            if response == False:
                json = await request.json() 
                await asyncio.sleep(json["retry_after"])
                await post_dm(limiter, headers, channel, message)

        