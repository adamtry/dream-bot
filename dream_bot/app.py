import json

from telegram_integration.telegram_bot import send_bot_message
import logging

logging.getLogger().setLevel(logging.INFO)


class LambdaEventInput:
    def __init__(self, event):
        self.event = event
        self.body = self.resolve_body()
        self.message = self.body.get("message")
        if self.message is None:
            raise Exception(f"No message in body {self.body}")

    def resolve_body(self) -> dict:
        logging.info(f"Raw event: {self.event}")
        try:
            if isinstance(self.event, str):
                # Throws TypeError if event is not a string
                body = json.loads(self.event)["body"]
            else:
                # Throws JSONDecodeError if event is not JSON
                body = json.loads(self.event["body"])
        except (TypeError, json.JSONDecodeError, KeyError):
            body = self.event["body"]
        if not isinstance(body, dict):
            body = json.loads(body)
        assert isinstance(body, dict), f"Invalid body type: {type(body)}"
        while "body" in body.keys():
            body = body["body"]
        logging.info(f"Event body: {body}")
        return body


def main(raw_event: str | dict):
    event = LambdaEventInput(raw_event)
    body = event.body
    chat_id = body["message"]["chat"]["id"]
    text = body["message"]["text"]
    send_bot_message(chat_id, text)


def lambda_handler(event: str | dict, context: object = None) -> dict:
    try:
        main(event)
        return {"statusCode": 200}
    except Exception as e:
        logging.error(e, exc_info=True)
        return {"statusCode": 500}
