from typing import Any, List

from discord import Colour, Embed, Message

from src.helpers import Helpers
from src.modules.store import Store


class Commands:
    """Contains all discord commands."""

    def __init__(self, helpers: Helpers, store: Store) -> None:
        self.helpers = helpers
        self.store = store

    async def man(self, message: Message, args: List) -> None:
        """Displays the help message."""
        embed = Embed(title="Hush | Help", colour=Colour.purple())

        prefix = self.helpers.config["general"]["prefix"]

        embed.add_field(
            name="General Commands", value=f"```{prefix}help```", inline=False
        )
        embed.add_field(
            name="Blacklist Commands:",
            value="**Prefix:** h!blacklist\n\n**Args**:\n*<word>*: The word to "
            "add or remove from the blacklist\n*<action>*: The type of "
            "action, accepted values are "
            "`alert`, `ban`, and `delete`\n\n```"
            "add <word> <action> | Blacklists a word\n"
            "remove <word> | Removes the word from the blacklist "
            "```",
            inline=False,
        )

        await message.channel.send(embed=embed)

    async def bl(self, message: Message, args: List) -> Any:
        """Handles the blacklist commands."""
        if not await self.helpers.has_args(args, 1, message):
            return False

        accepted_actions = ["add", "remove"]

        if args[0] not in accepted_actions:
            await message.channel.send(
                f"Action `{args[0]}` is not accepted. (Accepted options are {accepted_actions})"
            )
            return False

        if args[0] == "add":
            if not await self.helpers.has_args(args, 3, message):
                return False

            if self.store.add(args[1], args[2]):
                await message.channel.send(
                    f"**Added word to blacklist**\n\n*Word:* {args[1]}\n*Action:* {args[2]}"
                )
            else:
                await message.channel.send("Something went wrong while adding word.")

        elif args[0] == "remove":
            if not await self.helpers.has_args(args, 2, message):
                return True

            if self.store.remove(args[1]):
                await message.channel.send(
                    f"**Removed word from blacklist**:\n\n*Word:* {args[1]}"
                )
            else:
                await message.channel.send("Something went wrong while removing word.")
