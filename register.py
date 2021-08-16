import asyncio
from tkinter import *

from loguru import logger

from gui import update_tk, TkAppClosed
from helpers import load_config
from loginer import register
from sender import load_from_dotenv


new_nickname = None


def save_new_nickname(nick):
    global new_nickname
    new_nickname = nick.get()
    logger.debug(new_nickname)


async def register_new_nickname(user, hash):
    settings = load_config()
    global new_nickname
    while True:
        if new_nickname:
            logger.debug(f"Passing {new_nickname}")
            nickname, account_hash = await register(
                settings["host"],
                settings["sender_port"],
                new_nickname,
                watchdog_queue=None,
            )
            new_nickname = None
            logger.debug(nickname, account_hash)
            user.set(nickname)
            hash.set(account_hash)
        await asyncio.sleep(0)


async def create_window():
    account_hash, nickname = load_from_dotenv()
    if not nickname:
        nickname = "Anonymous"
    logger.debug(nickname)

    root = Tk()
    root.geometry("400x150")
    root.title("Nickname registration")

    Label(root, text="Username").grid(row=0, column=0)
    username_tk_object = StringVar()
    if nickname:
        username_tk_object.set(nickname)
    Entry(root, textvariable=username_tk_object).grid(row=0, column=1)

    Label(root, text="Account Hash").grid(row=1, column=0)
    hash_tk_object = StringVar()
    if account_hash:
        hash_tk_object.set(account_hash)
    Entry(root, textvariable=hash_tk_object, state=DISABLED).grid(row=1, column=1)

    Button(
        root,
        text="Save new nickname",
        command=lambda: save_new_nickname(username_tk_object),
    ).grid(row=4, column=0)

    await asyncio.gather(
        update_tk(root),
        register_new_nickname(username_tk_object, hash_tk_object),
    )


if __name__ == "__main__":
    try:
        asyncio.run(create_window())
    except TkAppClosed:
        pass
    # except KeyboardInterrupt:
    #     pass
