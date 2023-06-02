from . import commands
from . import telegram_usecases
from .domain_objects import TelegramMessage
from .telegram_gateway import TelegramBot


def handle_bot_message(bot: TelegramBot, message: TelegramMessage) -> None:
    """
    This function is called by the Lambda handler to handle a message from the Telegram bot.
    :param bot: The Telegram bot that received the message
    :param message: The message that was received
    """
    print(f"Message data: {message}")
    if message.forward_from or message.forward_from_chat:
        telegram_usecases.create_dream(bot, message)
    else:
        if commands.HELP_CMD in message.text or commands.START_CMD in message.text:
            help_message = commands.get_command_summary()
            bot.send_message(help_message)
        elif commands.SEARCH_DREAMS_CMD in message.text:
            telegram_usecases.search_dreams(bot, message)
        elif commands.DELETE_DREAM_CMD in message.text:
            telegram_usecases.delete_dream(bot, message)
        else:
            bot.send_message("Try /help for usage instructions")
    return
