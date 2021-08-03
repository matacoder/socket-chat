import asyncio
import json

from loguru import logger


async def chat_sender(host_, port_, uid, message=None):
    reader, writer = await asyncio.open_connection(host_, port_)

    # Obtain uid request
    welcome_message = await reader.readline()
    logger.debug(welcome_message.decode())

    # Send uid to log in
    writer.write(f"{uid}\n".encode())
    user_info = await reader.readline()

    user_info_dict = json.loads(user_info.decode())
    if not user_info_dict:
        logger.debug("Неизвестный токен. Проверьте его или зарегистрируйте заново.")
    else:
        logger.debug(user_info_dict)

        message = "Test message"
        while True:
            writer.write(f"{message}\n\n".encode())
            await asyncio.sleep(1)
        # writer.close()
