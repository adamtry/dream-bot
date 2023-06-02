import os
import uuid

from dynamodb import dynamodb_gateway, db_entities as entity
from .domain_objects import TelegramMessage
from .telegram_gateway import TelegramBot

DREAM_CHANNEL_ID = os.environ.get("DREAM_CHANNEL_ID")
assert DREAM_CHANNEL_ID is not None, "DREAM_CHANNEL_ID environment variable is not set"


def get_dream(bot, message):
    bot.send_message(f"Getting dream {message}")
    pass


def search_dreams(bot: TelegramBot, message: TelegramMessage):
    # Message format is /search_dreams <query>
    bot.send_message("Getting dreams")
    user_id = message.chat.id
    query = message.text.replace("/search_dreams", "").strip()
    dreams_for_user = dynamodb_gateway.search_dreams_for_user(user_id, query)
    if not dreams_for_user:
        bot.send_message("No dreams found")
        return
    bot.send_message(f"Found {len(dreams_for_user)} dreams")
    bot.send_message("\n\n".join([f"{dream.date} - *{dream.title}* - {dream.dream_id}" for dream in dreams_for_user]))


def delete_dream(bot, message):
    bot.send_message(f"Deleting dream {message}")
    pass


def create_dream(bot, message: TelegramMessage):
    # Only allow forwarding from dream channel
    if message.forward_from_chat and str(message.forward_from_chat.id) != DREAM_CHANNEL_ID:
        bot.send_message("Forward from chat but not dream channel")
        return
    if message.forward_from_chat and str(message.forward_from_chat.id) == DREAM_CHANNEL_ID:
        dream = entity.DreamEntity(
            dream_id=uuid.uuid4(),
            date=message.date,
            user_id=message.chat.id,
            username=message.chat.username,
            text=message.text,
        )
        assert dynamodb_gateway.add_dream(dream.to_db()), "🚨 Failed to add dream to database 🚨"
        bot.send_message(f"Dream added with title {dream.title} and id {dream.dream_id.hex}")
