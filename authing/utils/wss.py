# coding: utf-8

import websockets
import asyncio
async def connect(uri,func,authorization=None):
    headers = {"authorization":authorization} if authorization else {}
    try:
        async with websockets.connect(uri, extra_headers=headers) as websocket:
            print("connected ")
            async for message in websocket:
                func(message)
    except Exception as e:
        print(e)


def handleMessage(uri,func,authorization=None):
    asyncio.run(connect(uri,func,authorization))
