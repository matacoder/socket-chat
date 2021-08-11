from tkinter import *
from functools import partial

from loguru import logger

from sender import load_from_dotenv


def save_new_nickname(nick):
    """Saving nickname. Registration would be at first app run."""
    with open(".env", "w") as f:
        f.write(f"nickname={nick.get()}")


if __name__ == "__main__":

    account_hash, nickname = load_from_dotenv()
    logger.debug(nickname)
    # window
    root = Tk()
    root.geometry("400x150")
    root.title("Nickname saver.")

    # username label and text entry box
    user_label = Label(root, text="Username").grid(row=0, column=0)
    username_tk_object = StringVar()
    if nickname:
        username_tk_object.set(nickname)
    username_entry = Entry(root, textvariable=username_tk_object).grid(row=0, column=1)

    # password label and password entry box
    hash_label = Label(root, text="Account Hash").grid(row=1, column=0)
    hash_tk_object = StringVar()
    if account_hash:
        hash_tk_object.set(account_hash)
    password_entry = Entry(root, textvariable=hash_tk_object, state=DISABLED).grid(
        row=1, column=1
    )

    save_new_nickname = partial(save_new_nickname, username_tk_object)

    # login button
    login_button = Button(
        root, text="Save new nickname", command=save_new_nickname
    ).grid(row=4, column=0)

    root.mainloop()
