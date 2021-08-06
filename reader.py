import asyncio
import datetime

import aiofiles


async def chat_client_reader(host, port, log_file_name):
    """Stream messages from chat to stdout."""
    reader, writer = await asyncio.open_connection(host, port)

    try:
        while True:
            message = await reader.readline()
            current_formatted_datetime = datetime.datetime.now().strftime("[%Y.%m.%d %H:%M:%S]")
            message_with_timestamp = f"{current_formatted_datetime} {message.decode()}"
            async with aiofiles.open(log_file_name, "a") as chat_logs:
                await chat_logs.write(message_with_timestamp)
            print(message_with_timestamp.rstrip())
    finally:
        writer.close()
