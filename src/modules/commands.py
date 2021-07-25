from typing import Any, List

import discord
from discord import Colour, Embed, Message
from redis import Redis


async def bl_add(r: Redis, word: str, action: str, message: discord.Message) -> bool:
    """Adds a word from the blacklist."""
    try:
        r.set(word, action)
    except Exception as e:
        # TODO:: Add some kind of logging.
        await message.channel.send("Something went wrong.")
        return False

    await message.channel.send(
        f"**Added word to blacklist**\n\n*Word:* {word}\n*Action:* {action}"
    )
    return True


async def bl_remove(r: Redis, word: str, message: discord.Message) -> bool:
    """Removes a word from the blacklist."""
    try:
        r.delete(word)
    except Exception as e:
        # TODO:: Add some kind of logging.
        await message.channel.send("Something went wrong.")
        return False

    await message.channel.send(f"**Removed word from blacklist**:\n\n*Word:* {word}")
    return True


class Commands:
    """Contains all discord commands."""

    def __init__(self, helpers: Any) -> None:
        self.helpers = helpers

    async def man(self, message: Message, args: List, r: Redis) -> None:
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

    async def bl(self, message: Message, args: List, r: Redis) -> Any:
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

            return await bl_add(r, args[1], args[2], message)
        elif args[0] == "remove":
            if not await self.helpers.has_args(args, 2, message):
                return True

            return await bl_remove(r, args[1], message)
