
import os

from dotenv import load_dotenv


import gui
from loginer import authenticate
from helpers import sanitize_string

SETTINGS = {
    "host": "minechat.dvmn.org",
    "port": 5050,
}

writer = ""


async def create_connection(
    host, port, account_hash, nickname, status_updates_queue, watchdog_queue
):
    if status_updates_queue:
        status_updates_queue.put_nowait(gui.SendingConnectionStateChanged.INITIATED)
    global writer
    writer = await authenticate(host, port, account_hash, nickname)
    status_updates_queue.put_nowait(gui.SendingConnectionStateChanged.ESTABLISHED)
    watchdog_queue.put_nowait("Sending connection established.")
    return writer


async def initiate_connection_on_app_start(status_updates_queue, watchdog_queue):
    global writer
    account_hash, nickname = load_from_dotenv()
    writer = await create_connection(
        SETTINGS["host"],
        SETTINGS["port"],
        account_hash,
        nickname,
        status_updates_queue,
        watchdog_queue,
    )
    return writer


async def chat_sender(message, status_updates_queue, watchdog_queue):
    """Send message to chat after login or registration."""
    global writer
    if not writer:
        writer = await initiate_connection_on_app_start(status_updates_queue, watchdog_queue)

    sanitized_message = sanitize_string(message)

    writer.write(f"{sanitized_message}\n\n".encode())
    watchdog_queue.put_nowait("Message sent")


async def send_from_gui(sending_queue, status_updates_queue, watchdog_queue):
    """Send message from GUI."""
    account_hash, nickname = load_from_dotenv()
    event = gui.NicknameReceived(nickname)
    status_updates_queue.put_nowait(event)
    while True:
        message = await sending_queue.get()
        if message:
            await chat_sender(
                message,
                status_updates_queue,
                watchdog_queue,
            )


def load_from_dotenv():
    """Load saved nickname and hash to log in."""
    load_dotenv()
    return os.getenv("account_hash", None), os.getenv("nickname", None)
