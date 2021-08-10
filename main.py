import asyncio

import argparse
import datetime

from async_timeout import timeout
from loguru import logger

import gui
from reader import chat_client_reader
from sender import send_from_gui, initiate_connection_on_app_start
from anyio import sleep, create_task_group, run, ExceptionGroup, CancelScope


async def watch_for_connection(watchdog_queue):
    while True:
        try:
            async with timeout(5) as cm:
                message = await watchdog_queue.get()
                logger.debug(f"[{datetime.datetime.now().isoformat()}] {message}")
        except asyncio.TimeoutError:
            logger.debug("Timeout")
            raise ConnectionError


async def main2():
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
        watch_for_connection(watchdog_queue),
        initiate_connection_on_app_start(status_updates_queue, watchdog_queue),
    ]

    await asyncio.gather(*coroutines, return_exceptions=True)


async def main():
    messages_queue = asyncio.Queue()
    sending_queue = asyncio.Queue()
    status_updates_queue = asyncio.Queue()
    watchdog_queue = asyncio.Queue()
    while True:
        try:
            async with create_task_group() as tg:
                with CancelScope() as scope:
                    tg.start_soon(gui.draw, messages_queue, sending_queue, status_updates_queue)
                    tg.start_soon(
                        chat_client_reader,
                        args.host,
                        args.port,
                        args.logfile,
                        messages_queue,
                        status_updates_queue,
                        watchdog_queue,
                    )
                    tg.start_soon(
                        send_from_gui, sending_queue, status_updates_queue, watchdog_queue
                    )
                    tg.start_soon(watch_for_connection, watchdog_queue)
                    tg.start_soon(
                        initiate_connection_on_app_start, status_updates_queue, watchdog_queue
                    )
        except ConnectionError:
            await scope.cancel()
            logger.debug("Sleeping")
            await sleep(5)
            logger.debug("Reconnecting...")
        except ExceptionGroup:
            await scope.cancel()
            pass


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
        run(main)
    except KeyboardInterrupt:
        pass
