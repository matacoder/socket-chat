import asyncio

import aiofiles


async def chat_client():
    reader, writer = await asyncio.open_connection("minechat.dvmn.org", 5000)

    while True:
        message = await reader.readline()
        async with aiofiles.open("chat_logs.txt", "a") as chat_logs:
            await chat_logs.write(message.decode())
        print(message.decode())

    # writer.close()


if __name__ == "__main__":
    asyncio.run(chat_client())
