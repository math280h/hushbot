from dataclasses import dataclass
import re
from typing import Any, List, Pattern

from src.modules.store import Store


@dataclass
class CustomRule:
    """Dataclass for custom rules."""

    name: str
    action: str
    pattern: Pattern


class Filter:
    """Class for text filtering."""

    def __init__(self, store: Store, helper: Any) -> None:
        self.store = store
        self.helper = helper

        self.link_pattern = re.compile(
            r"(?:(?:https?|ftp):\/\/|\b(?:[a-z\d]+\.))(?:(?:[^\s()<>]+|\((?:[^\s()<>]+|(?:\([^\s()<>]+\)))?\))+("
            r"?:\((?:[^\s()<>]+|(?:\(?:[^\s()<>]+\)))?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))?/im"
        )

        self.custom_rules: List[CustomRule] = []
        self.compile_custom_rules()

    def compile_custom_rules(self) -> None:
        """Compile regex for all custom rules."""
        if "rules" in self.helper.config:
            for rule in self.helper.config["rules"]:
                rule_name = list(rule.keys())[0]
                self.custom_rules.append(
                    CustomRule(
                        rule_name,
                        rule[rule_name]["action"],
                        re.compile(rule[rule_name]["pattern"]),
                    )
                )

    async def filter(self, text: str) -> tuple:
        """Filter message content."""
        if self.custom_rules:
            for rule in self.custom_rules:
                if rule.pattern.match(text) is not None:
                    return (
                        rule.action,
                        f"Matched custom rule: {rule.name}",
                    )

        result = self.link_pattern.match(text)

        if result is not None:
            content = result[0]
        else:
            content = "".join(e for e in text if e.isalnum()).lower()

        for item in self.store.blacklist:
            if item.key in content:
                action = item.action
                return action, item.key

        return None, None
