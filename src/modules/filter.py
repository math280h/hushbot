import re
from typing import Any

from redis import Redis


class Filter:
    """Class for text filtering."""

    def __init__(self, r: Redis, helper: Any) -> None:
        self.r = r
        self.helper = helper

    async def filter(self, text: str) -> tuple:
        """Filter message content."""
        if "rules" in self.helper.config:
            for rule in self.helper.config["rules"]:
                rule_name = list(rule.keys())[0]
                if re.match(rule[rule_name]["pattern"], text) is not None:
                    return (
                        rule[rule_name]["action"],
                        f"Matched custom rule: {rule_name}",
                    )

        regex = (
            r"(?:(?:https?|ftp):\/\/|\b(?:[a-z\d]+\.))(?:(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))?\))+("
            r"?:\((?:[^\s()<>]+|(?:\(?:[^\s()<>]+\)))?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))?/im"
        )
        result = re.match(regex, text)

        if result is not None:
            content = result[0]
        else:
            content = "".join(e for e in text if e.isalnum()).lower()

        words = self.r.keys()

        for word in words:
            if word.decode().lower() in content:
                action = self.r.get(word.decode()).decode()
                return action, word.decode()

        return None, None
