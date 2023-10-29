import asyncio

from aiohttp import ClientSession
from .prettify import req_prettify as rp

async def send_message(limiter, session, channel, message):
    async with limiter:
        url = f"https://discord.com/api/v9/channels/{channel}/messages"
        payload = {"content": message}
        request = await session.post(url, json=payload, ssl=False)
        response = rp(request.status, url)
        if response == False:
            json = await request.json() 
            await asyncio.sleep(json["retry_after"])
            await send_message(limiter, session, channel, message)


async def spam_messages(limiter, headers, channel, message):
    async with ClientSession(headers=headers, connector=None) as session:
        #for _ in range(30):
            #await send_message(limiter, session, channel, message)
        tasks = [asyncio.create_task(send_message(limiter, session, channel, message)) for _ in range(30)]
        await asyncio.wait(tasks)