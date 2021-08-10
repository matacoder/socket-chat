import argparse
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


async def create_sender_connection(status_updates_queue, watchdog_queue):
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


async def chat_sender(message, watchdog_queue):
    """Send message to chat after login or registration."""
    global writer

    sanitized_message = sanitize_string(message)

    writer.write(f"{sanitized_message}\n\n".encode())
    # logger.debug(f"Sent message: {sanitized_message}")
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
                watchdog_queue,
            )


def load_from_dotenv():
    """Load saved nickname and hash to log in."""
    load_dotenv()
    return os.getenv("account_hash", None), os.getenv("nickname", None)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send message to private chat.")

    parser.add_argument("message", help="Specify message you want to send.")
    parser.add_argument(
        "-u",
        "--username",
        help="Specify username you want to use.",
        default="Anonymous",
    )
    parser.add_argument(
        "--host", help="Specify host to connect.", default=SETTINGS["host"]
    )
    parser.add_argument(
        "-p", "--port", help="Specify port to connect.", default=SETTINGS["port"]
    )

    args = parser.parse_args()

    load_dotenv()
    saved_account_hash, saved_nickname = load_from_dotenv()
    if not saved_nickname:
        saved_nickname = args.username

    sanitized_nickname = sanitize_string(saved_nickname)

    asyncio.run(
        chat_sender(
            args.host, args.port, saved_account_hash, sanitized_nickname, args.message
        )
    )
