from dataclasses import dataclass
from typing import List

from redis import Redis


@dataclass
class BlacklistedWord:
    """A Blacklisted word."""

    key: str
    action: str


class Store:
    """Handles data to/from redis."""

    def __init__(self, r: Redis) -> None:
        self.r = r

        self.blacklist: List[BlacklistedWord] = []
        self.load_from_redis()

    def load_from_redis(self) -> None:
        """Load blacklist from redis and store it in memory."""
        blacklist: List[BlacklistedWord] = []

        for item in self.r.keys():
            key: str = item.decode()

            blacklist.append(BlacklistedWord(key.lower(), self.r.get(key).decode()))

        # Overwrite current blacklist
        self.blacklist = blacklist

    def add(self, word: str, action: str) -> bool:
        """Adds a word from the blacklist."""
        try:
            self.r.set(word, action)
            self.load_from_redis()
            return True
        except Exception as e:
            # TODO:: Add some kind of logging.
            return False

    def remove(self, word: str) -> bool:
        """Removes a word from the blacklist."""
        try:
            self.r.delete(word)
            self.load_from_redis()
            return True
        except Exception as e:
            # TODO:: Add some kind of logging.
            return False
