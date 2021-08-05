import argparse
import asyncio
import os

from dotenv import load_dotenv
from loguru import logger

from loginer import authenticate
from helpers import string_sanitizer


async def chat_sender(host, port, account_hash, nickname, message=None):
    """Send message to chat after login or registration."""
    writer = await authenticate(host, port, account_hash, nickname)
    if not message:
        sanitized_message = "Test message"
    else:
        sanitized_message = string_sanitizer(message)

    writer.write(f"{sanitized_message}\n\n".encode())
    logger.debug(f"Sent message: {sanitized_message}")
    writer.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send message to private chat.")

    parser.add_argument("message", help="Specify message you want to send.")
    parser.add_argument("-u", "--username", help="Specify username you want to use.", default="Anonymous")
    parser.add_argument("--host", help="Specify host to connect.", default="minechat.dvmn.org")
    parser.add_argument("-p", "--port", help="Specify port to connect.", default=5050)

    args = parser.parse_args()

    load_dotenv()
    saved_account_hash = os.getenv("account_hash", None)
    saved_nickname = os.getenv("nickname", args.username)

    sanitized_nickname = string_sanitizer(saved_nickname)

    asyncio.run(chat_sender(args.host, args.port, saved_account_hash, sanitized_nickname, args.message))
