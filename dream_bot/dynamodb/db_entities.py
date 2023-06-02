import uuid
from dataclasses import dataclass
from datetime import date


@dataclass
class DreamEntity:
    dream_id: uuid.UUID
    # Store as date object
    date: date
    user_id: int
    username: str
    text: str
    title: str | None = None

    def __post_init__(self):
        if not self.title:
            # Use first line of text as title
            self.title: str = self.text.strip().split("\n")[0]
            self.text: str = "\n".join(self.text.strip().split("\n", 1)[1:])

    def to_db(self):
        return {
            "dream_id": self.dream_id.hex,
            "date": self.date.isoformat(),
            "user_id": self.user_id,
            "username": self.username.strip(),
            "title": self.title.strip(),
            "text": self.text.strip(),
        }
