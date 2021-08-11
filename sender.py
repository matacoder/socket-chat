import asyncio
import os

import async_timeout
from dotenv import load_dotenv
from loguru import logger

import gui
from loginer import authenticate
from helpers import sanitize_string

SETTINGS = {
    "host": "minechat.dvmn.org",
    "port": 5050,
}

reader = None
writer = None


async def connect_sender(status_updates_queue, watchdog_queue):
    account_hash, nickname = load_from_dotenv()
    status_updates_queue.put_nowait(gui.SendingConnectionStateChanged.INITIATED)
    global writer
    global reader
    reader, writer = await authenticate(
        SETTINGS["host"], SETTINGS["port"], account_hash, nickname, watchdog_queue
    )
    status_updates_queue.put_nowait(gui.SendingConnectionStateChanged.ESTABLISHED)
    watchdog_queue.put_nowait("Sending connection established.")
    return writer


async def ping_pong(watchdog_queue):
    global writer
    global reader
    while True:
        if writer and reader:
            try:
                async with async_timeout.timeout(15):
                    writer.write("\n".encode())
                    await writer.drain()
                    message = await reader.readline()
                    if message:
                        watchdog_queue.put_nowait(f"Pong, {message.decode()}")
            except TimeoutError:
                logger.debug("Ping timeout")
                raise
            except asyncio.CancelledError:
                logger.debug("Ping cancelled!")
                break
        await asyncio.sleep(5)



async def send_from_gui(sending_queue, status_updates_queue, watchdog_queue):
    """Send message from GUI."""
    account_hash, nickname = load_from_dotenv()
    event = gui.NicknameReceived(nickname)
    status_updates_queue.put_nowait(event)

    while True:
        if writer:
            try:
                message = await sending_queue.get()
                if message:
                    sanitized_message = sanitize_string(message)
                    writer.write(f"{sanitized_message}\n\n".encode())
                    await writer.drain()
                    watchdog_queue.put_nowait("Message sent")
            except asyncio.CancelledError:
                writer.close()
                logger.debug("Writing connection lost as well.")
                status_updates_queue.put_nowait(gui.SendingConnectionStateChanged.CLOSED)
                break
        else:
            await asyncio.sleep(0)


def load_from_dotenv():
    """Load saved nickname and hash to log in."""
    load_dotenv()
    return os.getenv("account_hash", None), os.getenv("nickname", None)
