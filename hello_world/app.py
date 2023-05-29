import json
from telegram_bot import send_bot_message
import logging

logging.getLogger().setLevel(logging.INFO)


def load_input(event: str | dict) -> dict:
    try:
        if isinstance(event, str):
            # Throws TypeError if event is not a string
            body = json.loads(event)["body"]
        else:
            # Throws JSONDecodeError if event is not JSON
            body = json.loads(event["body"])
    except (TypeError, json.JSONDecodeError):
        body = event["body"]
    return body


def main(event: str | dict):
    body = load_input(event)
    logging.info(f"Event body: {event['body']}")
    chat_id = body["message"]["chat"]["id"]
    text = body["message"]["text"]
    send_bot_message(chat_id, text)


def lambda_handler(event: str | dict, context: object = None) -> dict:
    try:
        main(event)
        return {"statusCode": 200}
    except Exception as e:
        logging.error(e, exc_info=True, stack_info=True)
        return {"statusCode": 500}
