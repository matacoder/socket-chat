import asyncio

import argparse

from reader import chat_client_reader


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

    asyncio.run(chat_client_reader(args.host, args.port, args.logfile))
