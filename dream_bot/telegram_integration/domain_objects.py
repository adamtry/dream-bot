from dataclasses import dataclass
from datetime import date


@dataclass
class TelegramUser:
    id: int
    is_bot: bool
    first_name: str
    last_name: str | None
    username: str | None


@dataclass
class TelegramChat:
    id: int
    type: str
    first_name: str | None
    last_name: str | None
    username: str | None


@dataclass
class MessageEntity:
    type: str
    offset: int
    length: int
    user: TelegramUser | None


@dataclass
class TelegramMessage:
    message_id: int
    text: str
    message_from: TelegramUser | None
    sender_chat: TelegramChat | None
    date: date
    chat: TelegramChat
    forward_from: TelegramUser | None
    forward_from_chat: TelegramChat | None
    entities: list[MessageEntity] | None
    document: dict | None

    def __repr__(self):
        formatted_date = self.date.strftime("%d.%m.%Y %H:%M:%S")
        return f"TelegramMessage(text={self.text}, message_from={self.message_from}, sender_chat={self.sender_chat}, " \
               f"date={formatted_date}, chat={self.chat}, forward_from={self.forward_from}, " \
               f"forward_from_chat={self.forward_from_chat}, entities={self.entities}, document={self.document})"
