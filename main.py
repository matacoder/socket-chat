import asyncio

import argparse
import datetime

from async_timeout import timeout
from loguru import logger

import gui
from reader import chat_client_reader
from sender import send_from_gui, create_sender_connection


async def handle_connection(watchdog_queue):
    while True:
        try:
            async with timeout(5) as cm:
                message = await watchdog_queue.get()
                logger.debug(f"[{datetime.datetime.now().isoformat()}] {message}")
            if cm.expired:
                break
        except asyncio.TimeoutError:
            logger.debug("Timeout")
            break


async def main():
    messages_queue = asyncio.Queue()
    sending_queue = asyncio.Queue()
    status_updates_queue = asyncio.Queue()
    watchdog_queue = asyncio.Queue()

    coroutines = [
        gui.draw(messages_queue, sending_queue, status_updates_queue),
        chat_client_reader(
            args.host,
            args.port,
            args.logfile,
            messages_queue,
            status_updates_queue,
            watchdog_queue,
        ),
        send_from_gui(sending_queue, status_updates_queue, watchdog_queue),
        handle_connection(watchdog_queue),
        create_sender_connection(status_updates_queue, watchdog_queue),
    ]

    await asyncio.gather(*coroutines, return_exceptions=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Connect to chat via socket.")
    parser.add_argument(
        "--host", help="Specify host to connect.", default="minechat.dvmn.org"
    )
    parser.add_argument("--port", help="Specify port to connect.", default=5000)
    parser.add_argument(
        "--logfile", help="Specify path to file to save logs.", default="chat_logs.txt"
    )

    args = parser.parse_args()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
