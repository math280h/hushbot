import logging
from os import getenv
from typing import Any

import discord
import redis

from src.helpers import Helpers
from src.modules.commands import Commands
from src.modules.filter import Filter
from src.modules.messenger import Messenger
from src.modules.store import Store


class Hush(discord.Client):
    """Main application class."""

    def __init__(self, **options: Any) -> None:

        super().__init__(**options)
        self.messenger = None
        self.commands = None

        self.ready = False

        # Initialize Logging
        self.logger = logging.getLogger("Hushbot")
        handler = logging.FileHandler("bot.log")
        log_format = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(log_format)
        self.logger.addHandler(handler)

        # Storage
        try:
            self.message_filter_storage = redis.Redis(
                host=getenv("REDIS_HOST"),
                port=getenv("REDIS_PORT"),
                username=getenv("REDIS_USER"),
                password=getenv("REDIS_PASS"),
            )
        except Exception:
            self.logger.exception("Exception occurred while initializing Redis")

        self.helpers = Helpers()
        self.store = Store(self.message_filter_storage, self.logger)
        self.msg_filter = Filter(self.store, self.helpers, self.logger)

    async def on_ready(self) -> None:
        """Handles messenger when connected to discord."""
        print("Connected!")
        print("Username: {0.name}\nID: {0.id}".format(self.user), flush=True)
        self.messenger = Messenger(
            self.get_channel(self.helpers.config["channels"]["log_channel"]),
            self.get_channel(self.helpers.config["channels"]["alert_channel"]),
        )

        self.commands = Commands(self.helpers, self.store, self.messenger, self.get_channel)

        self.ready = True

    async def on_message(self, message: discord.Message) -> None:
        """Handles messages."""
        if not self.ready:
            return

        if await self.helpers.is_command(
            message,
            discord.utils.get(
                message.guild.roles, id=self.helpers.config["permissions"]["staff_role"]
            ),
        ):
            command, args = await self.helpers.get_command(message)

            cmd_list = {
                "help": self.commands.man,
                "blacklist": self.commands.bl,
                "config": self.commands.config
            }

            cmd = cmd_list.get(command, self.commands.man)
            await cmd(message, args)

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
                await message.author.ban(
                    reason=f"Banned by Hushbot for the following message: {message.content}"
                )
                await self.messenger.notify(  # type: ignore
                    "Log", message.author.id, word, message.content, "Banned user"
                )
            elif result == "delete":
                await message.delete()
                await self.messenger.notify(  # type: ignore
                    "Log", message.author.id, word, message.content, "Deleted message"
                )
