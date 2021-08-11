import asyncio
import datetime
import socket

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
    try:
        reader, writer = await asyncio.open_connection(host, port)
        status_updates_queue.put_nowait(gui.ReadConnectionStateChanged.ESTABLISHED)
    except socket.gaierror:
        logger.debug("Reader gaierror")


async def load_chat_logs(messages_queue):
    log_file_name = READER_SETTINGS["logfile"]
    try:
        async with aiofiles.open(log_file_name, "r") as chat_logs:
            logs = await chat_logs.readlines()
            for log in logs[-10:]:
                messages_queue.put_nowait(log.rstrip())
    except FileNotFoundError:
        messages_queue.put_nowait("File with messages history not found.")


async def chat_client_reader(messages_queue, watchdog_queue, status_updates_queue):
    """Stream messages from chat to stdout."""
    log_file_name = READER_SETTINGS["logfile"]

    global reader
    global writer
    while True:
        if writer:
            try:
                message = await reader.readline()
                if message:
                    watchdog_queue.put_nowait("Message have been read from server.")
                    current_formatted_datetime = datetime.datetime.now().strftime(
                        "[%Y.%m.%d %H:%M:%S]"
                    )
                    message_with_datetime = (
                        f"{current_formatted_datetime} {message.decode()}"
                    )
                    async with aiofiles.open(log_file_name, "a") as chat_logs:
                        await chat_logs.write(message_with_datetime)
                    messages_queue.put_nowait(message_with_datetime.rstrip())
            except asyncio.CancelledError:
                writer.close()
                logger.debug("Close reader")
                status_updates_queue.put_nowait(gui.ReadConnectionStateChanged.CLOSED)
                break
        else:
            await asyncio.sleep(0)
