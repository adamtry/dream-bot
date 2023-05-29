import logging
import requests
import os

from dotenv import load_dotenv


class TelegramBot:
    def __init__(self):
        load_dotenv()
        token = os.environ.get("TELEGRAM_BOT_TOKEN")
        assert token is not None, "TELEGRAM_BOT_TOKEN environment variable is not set"
        self.TOKEN = token.strip()

        self.TELEGRAM_BASE_URL = f"https://api.telegram.org/bot{self.TOKEN}/"

        logging.info("Starting bot, token OK")

    def send_message(self, chat_id: str, text: str):
        logging.info(f"Sending message '{text}' to chat {chat_id}")
        url = self.TELEGRAM_BASE_URL + "sendMessage"
        data = {"chat_id": chat_id, "text": text}
        response = requests.post(url, data=data)
        response.raise_for_status()


def send_bot_message(chat_id, text) -> None:
    bot = TelegramBot()
    bot.send_message(chat_id, text)
    return {"statusCode": 200}
