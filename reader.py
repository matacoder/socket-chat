import asyncio
import datetime
import socket

import aiofiles
from async_timeout import timeout
from loguru import logger

import gui
from helpers import load_config


reader = None
writer = None


async def connect_reader(status_updates_queue):
    global reader
    global writer
    settings = load_config()
    host = settings["host"]
    port = settings["reader_port"]
    logger.debug(f"{host}:{port}")
    status_updates_queue.put_nowait(gui.ReadConnectionStateChanged.INITIATED)
    async with timeout(3):
        try:
            reader, writer = await asyncio.open_connection(host, port)
            status_updates_queue.put_nowait(gui.ReadConnectionStateChanged.ESTABLISHED)
        except socket.gaierror:
            logger.debug("Reader gaierror")


async def load_chat_logs(messages_queue):
    settings = load_config()
    log_file_name = settings["log_file_name"]
    try:
        async with aiofiles.open(log_file_name, "r") as chat_logs:
            logs = await chat_logs.readlines()
            for log in logs[-10:]:
                messages_queue.put_nowait(log.rstrip())
    except FileNotFoundError:
        messages_queue.put_nowait("File with messages history not found.")


async def write_to_log_file(log_queue: asyncio.Queue):
    settings = load_config()
    log_file_name = settings["log_file_name"]

    async with aiofiles.open(log_file_name, "a") as chat_logs:
        while True:
            message_with_datetime = await log_queue.get()
            await chat_logs.write(f"{message_with_datetime}\n")


async def chat_client_reader(
    messages_queue, watchdog_queue, status_updates_queue, log_queue
):
    """Stream messages from chat to stdout."""

    global reader
    global writer
    while True:
        logger.debug(f"Reader loop \n{reader}\n{writer}")
        if writer and reader:
            if not reader.at_eof():
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

                        messages_queue.put_nowait(message_with_datetime.rstrip())
                        log_queue.put_nowait(message_with_datetime.rstrip())
                except asyncio.CancelledError:
                    writer.close()
                    await writer.wait_closed()
                    status_updates_queue.put_nowait(
                        gui.ReadConnectionStateChanged.CLOSED
                    )
                    break

            else:
                await asyncio.sleep(3)
        else:
            await asyncio.sleep(3)
