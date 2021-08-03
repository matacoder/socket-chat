import asyncio
import datetime
import aiofiles


async def chat_client():
    reader, writer = await asyncio.open_connection("minechat.dvmn.org", 5000)

    while True:
        message = await reader.readline()
        timestamp = datetime.datetime.now().strftime("[%Y.%m.%d %H:%M:%S]")
        message_with_timestamp = f"{timestamp} {message.decode()}"
        async with aiofiles.open("chat_logs.txt", "a") as chat_logs:
            await chat_logs.write(message_with_timestamp)
        print(message_with_timestamp)

    # writer.close()


if __name__ == "__main__":
    asyncio.run(chat_client())
