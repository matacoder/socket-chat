import asyncio

import argparse

from reader import chat_client_reader


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Connect to chat via socket.")
    parser.add_argument("--host", help="Specify host to connect.")
    parser.add_argument("--port", help="Specify port to connect.")
    parser.add_argument("--history", help="Specify path to file to save logs.")

    args = parser.parse_args()
    host = args.host if args.host else "minechat.dvmn.org"
    port = args.port if args.port else 5000
    history = args.host if args.history else "chat_logs.txt"

    asyncio.run(chat_client_reader(host, port, history))
