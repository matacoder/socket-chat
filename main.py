import asyncio


import datetime

from async_timeout import timeout
from loguru import logger

import gui
from reader import chat_client_reader, connect_reader, load_chat_logs
from sender import send_from_gui, connect_sender, ping_pong
from anyio import (
    sleep,
    create_task_group,
    CancelScope,
    run,
)


async def watch_for_connection(watchdog_queue):
    while True:
        try:
            async with timeout(15):
                message = await watchdog_queue.get()
                logger.debug(f"[{datetime.datetime.now().isoformat()}] {message}")
        except asyncio.TimeoutError:
            logger.debug("Timeout")
            raise ConnectionError


async def handle_connection(
    messages_queue, sending_queue, status_updates_queue, watchdog_queue
):
    while True:
        try:
            async with create_task_group() as tg:
                with CancelScope() as scope:
                    tg.start_soon(connect_sender, status_updates_queue, watchdog_queue)
                    tg.start_soon(
                        connect_reader,
                        status_updates_queue,
                    )

                    tg.start_soon(
                        chat_client_reader,
                        messages_queue,
                        watchdog_queue,
                        status_updates_queue,
                    )
                    tg.start_soon(
                        send_from_gui,
                        sending_queue,
                        status_updates_queue,
                        watchdog_queue,
                    )
                    tg.start_soon(watch_for_connection, watchdog_queue)
                    tg.start_soon(ping_pong, watchdog_queue)

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

    async with create_task_group() as tg:
        tg.start_soon(gui.draw, messages_queue, sending_queue, status_updates_queue)
        tg.start_soon(load_chat_logs, messages_queue)
        tg.start_soon(
            handle_connection,
            messages_queue,
            sending_queue,
            status_updates_queue,
            watchdog_queue,
        )


if __name__ == "__main__":
    try:
        run(main)
    except (KeyboardInterrupt, gui.TkAppClosed):
        logger.debug("Closing")
        exit(0)
