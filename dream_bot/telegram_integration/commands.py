from dataclasses import dataclass


@dataclass
class Command:
    name: str
    description: str


@dataclass
class Commands:
    start = Command("/start", "Start the bot"),
    help = Command("/help", "Show help"),
    add_dream = Command("/add_dream", "Must be a reply to a message with the dream, usage /add_dream <dream title>"),
    list_dreams = Command("/list_dreams", "List all dreams for the user"),
    delete_dream = Command("/delete_dream", "Delete a dream, usage /delete_dream <dream title>"),
