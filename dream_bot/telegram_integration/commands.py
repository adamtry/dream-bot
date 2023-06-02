from dataclasses import dataclass


@dataclass
class Command:
    name: str
    description: str
    active: bool = True


START_CMD = "/start"
HELP_CMD = "/help"
GET_DREAM_CMD = "/get_dream"
SEARCH_DREAMS_CMD = "/search_dreams"
DELETE_DREAM_CMD = "/delete_dream"

COMMANDS = [
    Command(START_CMD, "Start the bot"),
    Command(HELP_CMD, "Show help"),
    Command(GET_DREAM_CMD, f"<dream id> - Get a dream"),
    Command(SEARCH_DREAMS_CMD, f"<optional query> - Search my dreams"),
    Command(DELETE_DREAM_CMD, f"<dream id> Delete a dream"),
]


def get_command_summary() -> str:
    summary = "Forward a dream from the dream channel to add it to your dream journal. " + \
              "Get dream IDs from the search dreams command\n"
    exclude = [START_CMD]
    for command in COMMANDS:
        if command.active and command.name not in exclude:
            summary += f"{command.name} - {command.description}\n"
    return summary


def get_command(name: str) -> Command | None:
    for command in COMMANDS:
        if command.name == name:
            return command
    return None
