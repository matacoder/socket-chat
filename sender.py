import argparse
import asyncio
import os

from dotenv import load_dotenv

from loginer import authenticate
from helpers import string_sanitizer


async def chat_sender(host_, port_, uid_, username_, message_=None):
    """Send message to chat after login or registration."""
    writer = await authenticate(host_, port_, uid_, username_)
    if not message_:
        message_ = "Test message"
    else:
        message_ = await string_sanitizer(message_)

    writer.write(f"{message_}\n\n".encode())
    writer.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send message to private chat.")

    parser.add_argument("message", help="Specify message you want to send")
    parser.add_argument("-u", "--username", help="Specify username you want to use.")
    parser.add_argument("--host", help="Specify host to connect.")
    parser.add_argument("-p", "--port", help="Specify port to connect.")

    args = parser.parse_args()
    host = args.host if args.host else "minechat.dvmn.org"
    port = args.port if args.port else 5050
    username = args.username if args.username else None
    message = args.message

    load_dotenv()
    uid = os.getenv("uid", None)
    if not username:
        username = os.getenv("username", "Anonymous")

    asyncio.run(chat_sender(host, port, uid, username, message))
