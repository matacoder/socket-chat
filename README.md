# Async Socket Reader and Writer

This program has been designed to async connect to Minecraft chat.

Test chat using netcat:
```bash
nc minechat.dvmn.org 5000
```

## Task description (in russian)

[DevMan Async CLI chat](https://dvmn.org/modules/async-python/lesson/underground-chat-cli/)

## Usage

Read the chat:

```bash
pyhton main.py
```

Send message to chat:

```bash
pyhton sender.py "This is message"
```