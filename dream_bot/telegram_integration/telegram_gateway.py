import os

import requests
from dotenv import load_dotenv

from .commands import Command, COMMANDS
from .domain_objects import TelegramChat

load_dotenv()  # for local development
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
assert TOKEN is not None, "TELEGRAM_BOT_TOKEN environment variable is not set"

BOT_BASE_URL = f"https://api.telegram.org/bot{TOKEN.strip()}"


def update_commands():
    commands: list[Command] = COMMANDS
    command_data = [
        {"command": command.name, "description": command.description} for command in commands
    ]
    url = BOT_BASE_URL + "/setMyCommands"
    data = {"commands": command_data}
    response = requests.post(url, data=data)
    response.raise_for_status()


class TelegramBot:
    def __init__(self, chat: TelegramChat):
        self.chat = chat
        print("Starting bot, token OK")

    def send_message(self, text: str):
        print(f"Sending message |✏️| '{text}' to chat {self.chat.id}")
        url = BOT_BASE_URL + "/sendMessage"
        data = {"chat_id": self.chat.id, "text": text}
        response = requests.post(url, data=data)
        response.raise_for_status()
