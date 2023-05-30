import os
from dataclasses import asdict

import requests
from dotenv import load_dotenv

from .commands import Command, Commands

load_dotenv()  # for local development
token = os.environ.get("TELEGRAM_BOT_TOKEN")
assert token is not None, "TELEGRAM_BOT_TOKEN environment variable is not set"
BOT_BASE_URL = f"https://api.telegram.org/bot{token.strip()}"


def update_commands():
    commands: list[Command] = list(asdict(Commands).values())
    command_data = [
        {"command": command.name, "description": command.description} for command in commands
    ]
    url = BOT_BASE_URL + "/setMyCommands"
    data = {"commands": command_data}
    response = requests.post(url, data=data)
    response.raise_for_status()


class TelegramBot:
    def __init__(self, chat_id: str):
        self.chat_id = chat_id
        print("Starting bot, token OK")

    def send_message(self, text: str):
        print(f"Sending message '{text}' to chat {self.chat_id}")
        url = BOT_BASE_URL + "/sendMessage"
        data = {"chat_id": self.chat_id, "text": text}
        response = requests.post(url, data=data)
        response.raise_for_status()
