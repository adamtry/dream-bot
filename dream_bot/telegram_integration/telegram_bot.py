from .domain_objects import TelegramMessage
from .telegram_gateway import TelegramBot


def handle_bot_message(message: TelegramMessage) -> None:
    bot = TelegramBot(message.chat.id)
    bot.send_message(message.text)
    print(f"Message data: {message}")
    if message.forward_from is None and message.forward_from_chat is None:
        bot.send_message("No forward from")
        return
    bot.send_message(f"Forward from: {message.forward_from}")
    bot.send_message(f"Forward from chat: {message.forward_from_chat}")
    return
