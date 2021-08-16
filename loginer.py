import asyncio
import json

import aiofiles
from loguru import logger

from helpers import TokenNotValidError

from tkinter import messagebox


async def save_user_to_dotenv(logged_user):
    """Save created user to .env file."""
    logger.debug("Saving...")
    account_hash_env = f"account_hash={logged_user['account_hash']}\n"
    username_env = f"nickname={logged_user['nickname']}"
    async with aiofiles.open(".env", "w") as dotenv:
        await dotenv.writelines(
            [
                account_hash_env,
                username_env,
            ]
        )


async def register(host, port, name, watchdog_queue=None):
    """Log in user, return login info dict."""
    logger.debug("Registering")
    try:
        reader, writer = await asyncio.open_connection(host, port)
    except ConnectionError:
        logger.debug("Register failed")
        raise

    welcome_message = await reader.readline()
    if watchdog_queue:
        watchdog_queue.put_nowait(welcome_message.decode())
    logger.debug(welcome_message)
    writer.write(f"\n".encode())
    await writer.drain()

    nickname_query = await reader.readline()
    if watchdog_queue:
        watchdog_queue.put_nowait(nickname_query.decode())

    if not name:
        name = "Anonymous"
    writer.write(f"{name}\n".encode())
    await writer.drain()

    logged_user_json = await reader.readline()
    logged_user = json.loads(logged_user_json.decode())
    if watchdog_queue:
        watchdog_queue.put_nowait(f"Created a new user: {logged_user}")
    await save_user_to_dotenv(logged_user)
    writer.close()

    return logged_user.values()


async def login(host, port, account_hash, watchdog_queue):
    """Log in user."""
    try:
        reader, writer = await asyncio.open_connection(host, port)
    except ConnectionError:
        logger.debug("Login failed")
        raise
    welcome_message = await reader.readline()
    watchdog_queue.put_nowait(welcome_message.decode())

    writer.write(f"{account_hash}\n".encode())
    await writer.drain()

    logged_user = await reader.readline()

    watchdog_queue.put_nowait(
        f"Attempt to log in with token returned: {logged_user.decode()}"
    )
    if not json.loads(logged_user.decode()):
        writer.close()

        messagebox.showinfo(
            "Token not valid.",
            "Check it or register again by deleting current token from .env file.",
        )
        exit()
        raise TokenNotValidError(
            "Token not valid. Check it or register again by deleting current token from .env file."
        )

    return reader, writer


async def authenticate(host, port, account_hash, name, watchdog_queue):
    """Login if possible or register new user."""
    if not account_hash:
        _, account_hash = await register(host, port, name, watchdog_queue)

    reader, writer = await login(host, port, account_hash, watchdog_queue)
    return reader, writer
