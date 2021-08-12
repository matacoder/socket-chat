# Async Socket Reader and Writer

This program has been designed to async connect to Minecraft chat.

<img src=https://raw.githubusercontent.com/matacoder/socket-chat/master/screenshots/main.png />

## Installation

Clone repository to your computer.

Create new virtual environment inside project folder:

```bash
python -m venv .venv
```

Install requirements:

```bash
python -m pip install -r requirements.txt
```

## Run GUI interface of the chat:

```bash
python -m main
```

### Create a username

Run separate script `register.py` and specify username. It will be registered at first app start.

<img src=https://raw.githubusercontent.com/matacoder/socket-chat/master/screenshots/register.png />

## Send message to chat:

Use GUI to send message

### Environment variables

App supports `.env` file with `nickname` you want to use and `account_hash` to log in.

You can specify it directly using `export nickname=NickName` bash command or using arguments.
