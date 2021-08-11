import asyncio

import argparse
import datetime

from async_timeout import timeout
from loguru import logger

import gui
from reader import chat_client_reader
from sender import send_from_gui, create_connection
from anyio import sleep, create_task_group, run, CancelScope


async def watch_for_connection(watchdog_queue):
    while True:
        try:
            async with timeout(5):
                message = await watchdog_queue.get()
                logger.debug(f"[{datetime.datetime.now().isoformat()}] {message}")
        except asyncio.TimeoutError:
            logger.debug("Timeout")
            global is_app_online
            raise ConnectionError


async def handle_connection(
    messages_queue, sending_queue, status_updates_queue, watchdog_queue
):
    while True:
        try:
            async with create_task_group() as tg:
                with CancelScope() as scope:
                    tg.start_soon(
                        create_connection, status_updates_queue, watchdog_queue
                    )
                    tg.start_soon(
                        chat_client_reader,
                        messages_queue,
                        status_updates_queue,
                        watchdog_queue,
                    )
                    tg.start_soon(
                        send_from_gui,
                        sending_queue,
                        status_updates_queue,
                        watchdog_queue,
                    )
                    tg.start_soon(watch_for_connection, watchdog_queue)

        except ConnectionError:
            await scope.cancel()
            logger.debug("Sleeping")
            await sleep(5)
            logger.debug("Reconnecting...")
        except BaseException as e:
            await scope.cancel()
            logger.debug(f"BaseException: {e}")
            await sleep(5)


async def main():
    messages_queue = asyncio.Queue()
    sending_queue = asyncio.Queue()
    status_updates_queue = asyncio.Queue()
    watchdog_queue = asyncio.Queue()

    asyncio.create_task(gui.draw(messages_queue, sending_queue, status_updates_queue))

    await handle_connection(
        messages_queue, sending_queue, status_updates_queue, watchdog_queue
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
