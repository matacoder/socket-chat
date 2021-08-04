import asyncio
import json

import aiofiles
from loguru import logger


async def save_hash_to_dotenv(logged_user):
    account_hash_env = f"uid={logged_user['account_hash']}\n"
    username_env = f"username={logged_user['nickname']}"
    async with aiofiles.open(".env", "w") as dotenv:
        await dotenv.writelines(
            [
                account_hash_env,
                username_env,
            ]
        )


async def register(host_, port_, name):
    """Log in user, return login info dict."""
    reader, writer = await asyncio.open_connection(host_, port_)

    await reader.readline()
    # "Hello %username%! Enter your personal hash or leave it empty to create new account."

    writer.write(f"\n".encode())

    await reader.readline()
    # "Enter preferred nickname below:"

    writer.write(f"{name}\n".encode())
    logged_user_json = await reader.readline()
    logged_user = json.loads(logged_user_json.decode())
    logger.debug(f"Created a new user: {logged_user}")
    await save_hash_to_dotenv(logged_user)
    writer.close()

    return logged_user["account_hash"]


async def login(host_, port_, account_hash, name):
    """Log in user."""

    reader, writer = await asyncio.open_connection(host_, port_)
    welcome_message = await reader.readline()
    # Hello %username%! Enter your personal hash or leave it empty to create new account.
    logger.debug(welcome_message.decode())

    writer.write(f"{account_hash}\n".encode())
    logged_user = await reader.readline()  # Return JSON NoneType if fails
    logger.debug(f"Attempt to log in with token returned: {logged_user}")
    if not json.loads(logged_user.decode()):
        writer.close()
        logger.debug("User token is not valid. Registering new one.")
        account_hash = await register(host_, port_, name=name)
        writer = await login(host_, port_, account_hash, name)
    return writer


async def authenticate(host_, port_, account_hash=None, name="James T. Kirk"):
    """Login if possible or register new user."""
    if not account_hash:
        account_hash = await register(host_, port_, name=name)

    writer = await login(host_, port_, account_hash, name=name)
    return writer
