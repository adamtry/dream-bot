import json
import traceback
from datetime import datetime

from dacite import from_dict

from telegram_integration.telegram_bot import handle_bot_message
from telegram_integration.telegram_gateway import TelegramBot, update_commands
from telegram_integration.domain_objects import TelegramMessage


class LambdaEventInput:
    def __init__(self, event: str | dict):
        self.event = event
        self.body = self.resolve_body(self.event)
        message: dict | None = self.body.get("message")
        if message is None:
            raise Exception(f"No message in body {self.body}")
        self.message: dict = message

    @staticmethod
    def resolve_body(event: str | dict) -> dict:
        # This method is to handle the different ways that the Lambda can receive events (API Gateway, Postman, Local run, etc.)
        # logging.info(f"Raw event: {event}")
        body = None
        try:
            if isinstance(event, str):
                # Throws TypeError if event is not a string
                body = json.loads(event)["body"]
            else:
                # Throws JSONDecodeError if event is not JSON
                body = json.loads(event["body"])
        except (TypeError, json.JSONDecodeError, KeyError):
            if isinstance(event, dict):
                body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)
        assert isinstance(body, dict), f"Invalid body type: {type(body)}"
        while "body" in body.keys():
            body = body["body"]
        # logging.info(f"Event body: {body}")
        return body


def main(raw_event: str | dict):
    event = LambdaEventInput(raw_event)
    telegram_message = from_dict(data_class=TelegramMessage, data=event.message)
    handle_bot_message(telegram_message)


def lambda_handler(event: str | dict, context: object = None) -> dict:
    print(f"\n=🚀= START {datetime.now().strftime('%H:%M:%S')} =🚀=")
    try:
        main(event)
        status = {"statusCode": 200}
    except Exception as e:
        print(f"Failed to parse event{event}. Stacktrace: {e}")
        traceback.print_exc()
        status = {"statusCode": 500}
    finally:
        print(f"\n=🔕= END {datetime.now().strftime('%H:%M:%S')} =🔕=")
        return status


if __name__ == "__main__":
    bot = TelegramBot()
    update_commands()
