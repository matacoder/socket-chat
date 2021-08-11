import asyncio
import os

from dotenv import load_dotenv
from loguru import logger

import gui
from loginer import authenticate
from helpers import sanitize_string

SETTINGS = {
    "host": "minechat.dvmn.org",
    "port": 5050,
}

writer = None


async def connect_sender(status_updates_queue, watchdog_queue):
    account_hash, nickname = load_from_dotenv()
    status_updates_queue.put_nowait(gui.SendingConnectionStateChanged.INITIATED)
    global writer
    writer = await authenticate(
        SETTINGS["host"], SETTINGS["port"], account_hash, nickname, watchdog_queue
    )
    status_updates_queue.put_nowait(gui.SendingConnectionStateChanged.ESTABLISHED)
    watchdog_queue.put_nowait("Sending connection established.")
    return writer


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
