import asyncio
import datetime

import aiofiles


async def chat_client_reader(host_, port_, history_):
    reader, writer = await asyncio.open_connection(host_, port_)

    try:
        while True:
            message = await reader.readline()
            timestamp = datetime.datetime.now().strftime("[%Y.%m.%d %H:%M:%S]")
            message_with_timestamp = f"{timestamp} {message.decode()}"
            async with aiofiles.open(history_, "a") as chat_logs:
                await chat_logs.write(message_with_timestamp)
            print(message_with_timestamp)
    except KeyboardInterrupt:
        writer.close()
