from typing import Any, List, Callable

from discord import Colour, Embed, Message, utils

from src.helpers import Helpers
from src.modules.store import Store
from src.modules.messenger import Messenger


class Commands:
    """Contains all discord commands."""

    def __init__(self, helpers: Helpers, store: Store, messenger: Messenger, get_channel: Callable) -> None:
        self.helpers = helpers
        self.store = store
        self.messenger = messenger
        self.get_channel = get_channel

    async def man(self, message: Message, args: List) -> None:
        """Displays the help message."""
        embed = Embed(title="Hush | Help", colour=Colour.purple())

        prefix = self.helpers.config["general"]["prefix"]

        embed.add_field(
            name="General Commands", value=f"```{prefix}help```", inline=False
        )
        embed.add_field(
            name="Blacklist Commands:",
            value=f"**Prefix:** {prefix}blacklist\n\n**Args**:\n*<word>*: The word to "
            "add or remove from the blacklist\n*<action>*: The type of "
            "action, accepted values are "
            "`alert`, `ban`, and `delete`\n\n```"
            "add <word> <action> | Blacklists a word\n"
            "remove <word> | Removes the word from the blacklist\n"
            "show | Shows the current blacklist"
            "```",
            inline=False,
        )

        embed.add_field(
            name="Config Commands:",
            value=f"**Prefix:** {prefix}config <option>\n\n**Args**:\n*<option>*: The option you "
                  "want to configure, accepted values are `prefix`, `channels`, `permissions`, `rules`\n\n```"
                  "prefix | Prefix\n"
                  "channels | Channels\n"
                  "permissions | Permissions"
                  "rules | Custom rules"
                  "```",
            inline=False,
        )

        await message.channel.send(embed=embed)

    async def bl(self, message: Message, args: List) -> Any:
        """Handles the blacklist commands."""
        if not await self.helpers.has_args(args, 1, message):
            return False

        accepted_actions = ["add", "remove", "show"]

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

        elif args[0] == "show":
            try:
                embed = Embed(title="Hush | Blacklist", colour=Colour.purple())
                output = ""
                for word in self.store.blacklist:
                    output += f"**{word.key}** - {word.action}\n"

                embed.add_field(
                    name="Currently Blacklisted",
                    value=f"Shown as `Word - Action`\n\n{output}",
                    inline=False,
                )

                await message.channel.send(embed=embed)

            except Exception:
                await message.channel.send("Something went wrong while showing list.")

    async def config(self, message: Message, args: List) -> Any:
        """Handles the blacklist commands."""
        if not await self.helpers.has_args(args, 1, message):
            return False

        accepted_actions = ["prefix", "channels", "permissions", "rules"]

        if args[0] not in accepted_actions:
            await message.channel.send(
                f"Action `{args[0]}` is not accepted. (Accepted options are {accepted_actions})"
            )
            return False

        if args[0] == "prefix":
            if not await self.helpers.has_args(args, 2, message):
                return False

            self.helpers.config["general"]["prefix"] = args[1]
            await message.channel.send(f"Prefix configured to: {args[1]}")

        elif args[0] == "channels":
            if not await self.helpers.has_args(args, 3, message):
                return False

            accepted_channels = ["log", "alert"]
            if args[1] not in accepted_channels:
                await message.channel.send(
                    f"Channel `{args[1]}` is not accepted. (Accepted options are {accepted_channels}"
                )
                return False

            if not args[2].startswith("<#"):
                await message.channel.send(f"Invalid channel: {args[2]}")
                return False

            channel = args[2][2:20]
            discord_channel = self.get_channel(int(channel))

            if args[1] == "log":
                self.helpers.config["channels"]["log_channel"] = channel
                self.messenger.log_channel = discord_channel
                await message.channel.send(f"Log channel configured to: <#{channel}>")
            elif args[1] == "alert":
                self.helpers.config["channels"]["alert_channel"] = channel
                self.messenger.alert_channel = discord_channel
                await message.channel.send(f"Alert channel configured to: <#{channel}>")

        elif args[0] == "permissions":
            if not await self.helpers.has_args(args, 3, message):
                return False

            if args[1] == "staff":
                if args[2].startswith("<@&"):
                    role = args[2][3:21]
                    self.helpers.config["permissions"]["staff_role"] = role
                    await message.channel.send(f"Staff role configured to: <@&{role}>")
                else:
                    await message.channel.send(f"Invalid staff role: {args[2]}")
            else:
                await message.channel.send(f"Invalid permission type: {args[1]} (Accepted: staff)")

        elif args[0] == "rules":
            await message.channel.send("Rule config")
