from os import getenv
from typing import Any

import discord
import redis

from src.helpers import Helpers
from src.modules.commands import Commands
from src.modules.filter import Filter
from src.modules.messenger import Messenger


class Hush(discord.Client):
    """Main application class."""

    def __init__(self, **options: Any) -> None:

        super().__init__(**options)
        self.messenger = None

        # Storage
        self.message_filter_storage = redis.Redis(
            host=getenv("REDIS_HOST"),
            port=getenv("REDIS_PORT"),
            username=getenv("REDIS_USER"),
            password=getenv("REDIS_PASS"),
        )

        self.helpers = Helpers()
        self.msg_filter = Filter(self.message_filter_storage, self.helpers)
        self.commands = Commands(self.helpers)

    async def on_ready(self) -> None:
        """Handles messenger when connected to discord."""
        print("Connected!")
        print("Username: {0.name}\nID: {0.id}".format(self.user))
        self.messenger = Messenger(
            self.get_channel(self.helpers.config["channels"]["log_channel"]),
            self.get_channel(self.helpers.config["channels"]["alert_channel"]),
        )

    async def on_message(self, message: discord.Message) -> None:
        """Handles messages."""
        if await self.helpers.is_command(
            message,
            discord.utils.get(
                message.guild.roles, id=self.helpers.config["permissions"]["staff_role"]
            ),
        ):
            command, args = await self.helpers.get_command(message)

            cmd_list = {"help": self.commands.man, "blacklist": self.commands.bl}

            cmd = cmd_list.get(command, self.commands.man)
            await cmd(message, args, self.message_filter_storage)

        elif not message.author.bot:
            # Filter messages
            result, word = await self.msg_filter.filter(message.content)

            if result is None:
                # Nothing wrong detected with this message
                return
            elif result == "alert":
                await self.messenger.notify(  # type: ignore
                    "Alert", message.author.id, word, message.content
                )
            elif result == "ban":
                await self.messenger.notify(  # type: ignore
                    "Log", message.author.id, word, message.content, "Banned user"
                )
            elif result == "delete":
                await message.delete()
                await self.messenger.notify(  # type: ignore
                    "Log", message.author.id, word, message.content, "Deleted message"
                )
