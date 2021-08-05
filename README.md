# Async Socket Reader and Writer

This program has been designed to async connect to Minecraft chat.

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

## Read the chat:

```bash
python -m main
```

### Additional arguments:

`--host` to specify host to connect.

`--port` to specify port to connect.

`--history` to specify path to file to save logs.

## Send message to chat:

```bash
python -m sender "This is message"
```

### Additional arguments:

`-u` or `--username` to specify username you want to use.

`--host` to specify host to connect.

`-p` or `--port` to specify port to connect.



## Task description 

[DevMan Async CLI chat (in russian)](https://dvmn.org/modules/async-python/lesson/underground-chat-cli/)

Test chat using netcat:
```bash
nc minechat.dvmn.org 5000
```