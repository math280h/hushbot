from discord import Embed, Colour
from redis import Redis


async def bl_add(r: Redis, word, action):
    r.set(word, action)
    return True


async def bl_remove(r: Redis, word):
    r.delete(word)
    return True


class Commands:
    def __init__(self, helpers):
        self.helpers = helpers

    async def man(self, message, args, r: Redis):
        embed = Embed(title="Hush | Help", colour=Colour.purple())

        prefix = self.helpers.config["general"]["prefix"]

        embed.add_field(
            name=f"General Commands",
            value=f"```{prefix}help```",
            inline=False
        )
        embed.add_field(
            name=f"Blacklist Commands:",
            value="**Prefix:** h!blacklist\n\n**Args**:\n*<word>*: The word to "
                  "add or remove from the blacklist\n*<action>*: The type of "
                  "action, accepted values are "
                  "`alert`, `ban`, and `delete`\n\n```"
                  f"add <word> <action> | Blacklists a word\n"
                  f"remove <word> | Removes the word from the blacklist "
                  "```",
            inline=False
        )

        await message.channel.send(embed=embed)

    async def bl(self, message, args, r: Redis):
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

            return await bl_add(r, args[1], args[2])
        elif args[0] == "remove":
            if not await self.helpers.has_args(args, 2, message):
                return True

            return await bl_remove(r, args[1])
