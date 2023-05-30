import logging
from dataclasses import asdict

import requests
import os

from dotenv import load_dotenv
from .commands import Commands


class TelegramBot:
    def __init__(self):
        load_dotenv()
        token = os.environ.get("TELEGRAM_BOT_TOKEN")
        assert token is not None, "TELEGRAM_BOT_TOKEN environment variable is not set"
        self.TOKEN = token.strip()

        self.TELEGRAM_BASE_URL = f"https://api.telegram.org/bot{self.TOKEN}"

        logging.info("Starting bot, token OK")

    def send_message(self, chat_id: str, text: str):
        logging.info(f"Sending message '{text}' to chat {chat_id}")
        url = self.TELEGRAM_BASE_URL + "/sendMessage"
        data = {"chat_id": chat_id, "text": text}
        response = requests.post(url, data=data)
        response.raise_for_status()

    def update_commands(self):
        commands = asdict(Commands)
        command_data = [
            {"command": command.name, "description": command.description}
            for command in commands
        ]
        url = self.TELEGRAM_BASE_URL + "/setMyCommands"
        data = {"commands": command_data}
        response = requests.post(url, data=data)


def send_bot_message(chat_id, text) -> None:
    bot = TelegramBot()
    bot.send_message(chat_id, text)
    return
