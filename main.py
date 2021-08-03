import asyncio
import datetime
import aiofiles
import argparse

from sender import chat_sender


async def chat_client_reader(host_, port_, history_):
    reader, writer = await asyncio.open_connection(host_, port_)

    while True:
        message = await reader.readline()
        timestamp = datetime.datetime.now().strftime("[%Y.%m.%d %H:%M:%S]")
        message_with_timestamp = f"{timestamp} {message.decode()}"
        async with aiofiles.open(history_, "a") as chat_logs:
            await chat_logs.write(message_with_timestamp)
        print(message_with_timestamp)

    # writer.close()


async def main():
    await asyncio.gather(
        chat_sender(host, 5050, "a357016c-f451-11eb-8c47-0242ac110002"),
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

    asyncio.run(main())
