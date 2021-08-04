import asyncio
import os

import argparse

from reader import chat_client_reader
from sender import chat_sender
from dotenv import load_dotenv


async def main():
    await asyncio.gather(
        chat_sender(host, 5050, uid),
        chat_client_reader(host, port, history),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Connect to chat via socket.")
    parser.add_argument("--host", help="Specify host to connect.")
    parser.add_argument("--port", help="Specify port to connect.")
    parser.add_argument("--history", help="Specify path to file to save logs.")

    args = parser.parse_args()
    host = args.host if args.host else "minechat.dvmn.org"
    port = args.port if args.port else 5000
    history = args.host if args.history else "chat_logs.txt"
    load_dotenv()
    uid = os.getenv("uid")

    asyncio.run(main())
