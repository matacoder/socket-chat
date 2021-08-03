import asyncio


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection("minechat.dvmn.org", 5000)

    print(f"Send: {message!r}")
    writer.write(message.encode())
    while True:
        data = await reader.read(1000)
        print(f"{data.decode()}")

    # writer.close()


if __name__ == "__main__":
    asyncio.run(tcp_echo_client("Hello World!"))
