import asyncio
import json

from loguru import logger

from loginer import authenticate


async def chat_sender(host_, port_, uid, message=None):
    writer = await authenticate(host_, port_, uid)
    message = "Test message"
    try:
        while True:
            writer.write(f"{message}\n\n".encode())
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        writer.close()
