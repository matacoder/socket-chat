import asyncio
import json

import aiofiles
from loguru import logger

from helpers import TokenNotValidError


async def save_user_to_dotenv(logged_user):
    """Save created user to .env file."""
    account_hash_env = f"uid={logged_user['account_hash']}\n"
    username_env = f"username={logged_user['nickname']}"
    async with aiofiles.open(".env", "w") as dotenv:
        await dotenv.writelines(
            [
                account_hash_env,
                username_env,
            ]
        )


async def register(host, port, name):
    """Log in user, return login info dict."""
    reader, writer = await asyncio.open_connection(host, port)

    welcome_message = await reader.readline()
    logger.debug(welcome_message.decode())

    writer.write(f"\n".encode())
    await writer.drain()

    nickname_query = await reader.readline()
    logger.debug(nickname_query.decode())

    if not name:
        name = "Anonymous"
    writer.write(f"{name}\n".encode())
    await writer.drain()

    logged_user_json = await reader.readline()
    logged_user = json.loads(logged_user_json.decode())
    logger.debug(f"Created a new user: {logged_user}")
    await save_user_to_dotenv(logged_user)
    writer.close()

    return logged_user["account_hash"]


async def login(host, port, account_hash):
    """Log in user."""
    reader, writer = await asyncio.open_connection(host, port)
    welcome_message = await reader.readline()
    logger.debug(welcome_message.decode())

    writer.write(f"{account_hash}\n".encode())
    await writer.drain()

    logged_user = await reader.readline()

    logger.debug(f"Attempt to log in with token returned: {logged_user.decode()}")
    if not json.loads(logged_user.decode()):
        writer.close()
        raise TokenNotValidError(
            "Token not valid. Check it or register again by deleting current token from .env file."
        )
    return writer


async def authenticate(host, port, account_hash, name):
    """Login if possible or register new user."""
    if not account_hash:
        account_hash = await register(host, port, name)

    writer = await login(host, port, account_hash)
    return writer
