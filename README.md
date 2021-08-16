# Async Socket Reader and Writer

This program has been designed to async connect to Minecraft chat.

<img src=https://user-images.githubusercontent.com/67960818/129526168-5c7625a4-334e-44f5-a6d0-1ea97c29cbf2.png />

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

<img src=https://user-images.githubusercontent.com/67960818/129526163-6ea3e222-0199-494a-9054-121562a7def1.png />

## Send message to chat:

Use GUI to send message

### Environment variables

App supports `.env` file with `nickname` you want to use and `account_hash` to log in.

You can specify it directly using `export nickname=NickName` bash command or using arguments.

## Settings

You can modify connection settings in `settings.toml`

Default values:

```toml
[DEFAULT]
host: minechat.dvmn.org
logfile: chat_logs.txt
[READER]
port: 5000
[SENDER]
port: 5050
```