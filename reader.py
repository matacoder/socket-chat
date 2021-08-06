import asyncio
import datetime

import aiofiles

import gui


async def chat_client_reader(
    host, port, log_file_name, messages_queue, status_updates_queue
):
    """Stream messages from chat to stdout."""
    status_updates_queue.put_nowait(gui.ReadConnectionStateChanged.INITIATED)
    reader, writer = await asyncio.open_connection(host, port)
    status_updates_queue.put_nowait(gui.ReadConnectionStateChanged.ESTABLISHED)

    try:
        while True:
            message = await reader.readline()
            current_formatted_datetime = datetime.datetime.now().strftime(
                "[%Y.%m.%d %H:%M:%S]"
            )
            message_with_datetime = f"{current_formatted_datetime} {message.decode()}"
            async with aiofiles.open(log_file_name, "a") as chat_logs:
                await chat_logs.write(message_with_datetime)
            print(message_with_datetime.rstrip())
            messages_queue.put_nowait(message_with_datetime.rstrip())
    finally:
        writer.close()
        status_updates_queue.put_nowait(gui.ReadConnectionStateChanged.CLOSED)
