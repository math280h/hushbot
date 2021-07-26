from typing import Dict, List

import discord
from schema import Optional, Schema, SchemaError
import yaml


def load_config() -> Dict:
    """Loads and validates 'config.yaml'."""
    config_schema = Schema(
        {
            "hushbot": {
                "general": {"prefix": str},
                "channels": {"log_channel": int, "alert_channel": int},
                "permissions": {"staff_role": int},
                Optional("rules"): [object],
            }
        }
    )

    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

        try:
            config_schema.validate(config)
        except SchemaError as se:
            raise se

        return config["hushbot"]


async def is_staff(user: discord.Member, required_role: discord.Role) -> bool:
    """Makes sure the user has the configured staff role."""
    return required_role in user.roles


class Helpers:
    """Contains small helper functions."""

    def __init__(self) -> None:
        self.config = load_config()

    async def is_command(
        self, message: discord.Message, required_role: discord.Role
    ) -> bool:
        """Checks if the input message is a command."""
        return (
            message.content.startswith(self.config["general"]["prefix"])
            and not message.author.bot
            and await is_staff(message.author, required_role)
        )

    async def get_command(self, message: discord.Message) -> tuple[str, List[str]]:
        """Get's the specified command from message."""
        ctx = message.content[len(self.config["general"]["prefix"]) :].split(" ")
        return ctx[0], ctx[1:]

    async def has_args(
        self, args: List, expected: int, message: discord.Message
    ) -> bool:
        """Checks if the list of args matches the expected amount of args."""
        if len(args) >= expected:
            return True

        await message.channel.send("Missing args")
        return False
