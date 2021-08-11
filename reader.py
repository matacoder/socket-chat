import asyncio
import datetime

import aiofiles
from async_timeout import timeout
from loguru import logger

import gui


READER_SETTINGS = {
    "host": "minechat.dvmn.org",
    "port": 5000,
    "logfile": "chat_logs.txt",
}

reader = None
writer = None


async def connect_reader(status_updates_queue):
    global reader
    global writer
    host, port, _ = READER_SETTINGS.values()
    logger.debug(f"{host}:{port}")
    status_updates_queue.put_nowait(gui.ReadConnectionStateChanged.INITIATED)
    reader, writer = await asyncio.open_connection(host, port)
    status_updates_queue.put_nowait(gui.ReadConnectionStateChanged.ESTABLISHED)



async def chat_client_reader(messages_queue, watchdog_queue, status_updates_queue):
    """Stream messages from chat to stdout."""
    log_file_name = READER_SETTINGS["logfile"]
    try:
        async with aiofiles.open(log_file_name, "r") as chat_logs:
            logs = await chat_logs.readlines()
            for log in logs:
                messages_queue.put_nowait(log.rstrip())
    except FileNotFoundError:
        messages_queue.put_nowait("File with messages history not found.")
    global reader
    global writer
    while True:
        try:
            message = await reader.readline()
            watchdog_queue.put_nowait("Message have been read from server.")
            current_formatted_datetime = datetime.datetime.now().strftime(
                "[%Y.%m.%d %H:%M:%S]"
            )
            message_with_datetime = f"{current_formatted_datetime} {message.decode()}"
            async with aiofiles.open(log_file_name, "a") as chat_logs:
                await chat_logs.write(message_with_datetime)
            messages_queue.put_nowait(message_with_datetime.rstrip())
        except asyncio.CancelledError:
            writer.close()
            logger.debug("Close reader")
            status_updates_queue.put_nowait(gui.ReadConnectionStateChanged.CLOSED)
            break
