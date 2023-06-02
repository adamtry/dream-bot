import json
import traceback
from datetime import datetime
from zoneinfo import ZoneInfo

import dacite.exceptions
from dacite import from_dict

from telegram_integration.domain_objects import TelegramMessage, TelegramChat
from telegram_integration.telegram_gateway import TelegramBot
from telegram_integration.telegram_handler import handle_bot_message


class MessageProcessingError(Exception):
    pass


class LambdaEventInput:
    def __init__(self, event: str | dict):
        self.event = event
        self.body = self.resolve_body(self.event)
        self.message: dict = self.body.get("message") if self.body else None

    @staticmethod
    def resolve_body(event: dict) -> dict:
        # event is a dict but message is a json string
        try:
            body: dict = json.loads(event['body'])
        except json.decoder.JSONDecodeError:
            raise MessageProcessingError(f"Failed to parse event body: {event}")
        return body


def make_telegram_bot_from_event(raw_event: str | dict) -> TelegramBot:
    try:
        data = raw_event.get("body").get("message").get("chat")
    except AttributeError:
        return None
    chat = dacite.from_dict(data_class=TelegramChat, data=data)
    telegram_bot = TelegramBot(chat)
    return telegram_bot


def lambda_handler(event: dict, context: object = None) -> dict:
    def get_british_time():
        return datetime.now(ZoneInfo("Europe/London")).strftime('%H:%M:%S')

    def end_execution(tg_bot: TelegramBot | None, status_code: int = 200, message: str = None):
        if status_code != 200:
            traceback.print_exc()
        if message is not None:
            print(message)
            if TelegramBot:
                print(tg_bot)
                tg_bot.send_message(message)
        return {"statusCode": status_code}

    bot = None
    try:
        print(f"=🚀= START {get_british_time()} =🚀=")
        print(json.dumps(event.get("body")))
        lambda_event = LambdaEventInput(event)
        chat = from_dict(data_class=TelegramChat, data=lambda_event.message.get("chat"))
        bot = TelegramBot(chat)
        if bot is None:
            raise MessageProcessingError(f"Invalid event: {event}")

        if lambda_event.message is None:
            print(f"No message found in event: {lambda_event.event}")
            raise MessageProcessingError(f"No message found in event: {lambda_event.event}")
        lambda_event.message["date"] = datetime.fromtimestamp(lambda_event.message["date"]).date()
        telegram_message = from_dict(data_class=TelegramMessage, data=lambda_event.message)
        handle_bot_message(bot, telegram_message)
        return end_execution(bot, 200, " 🟢 Complete ")
    except dacite.exceptions.MissingValueError as e:
        return end_execution(bot, 400, f" 🚨 Failed to parse message body. 🚨 Reason: {e}")
    except MessageProcessingError as e:
        return end_execution(bot, 400, f" 🚨 Failed to process message. 🚨 Reason: {e}")
    except Exception as e:
        return end_execution(bot, 500, f" 🚨 Failed. 🚨 Reason: {e}")
    finally:
        print(f"=🔕= END {get_british_time()} =🔕=")
