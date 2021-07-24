import discord
import yaml
from schema import Schema, SchemaError

from typing import Dict


def load_config() -> Dict:
    config_schema = Schema({
        "hushbot": {
            "general": {
                "prefix": str
            },
            "channels": {
                "log_channel": int,
                "alert_channel": int
            },
            "permissions": {
                "staff_role": int
            }
        }
    })

    with open('config.yaml', 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

        try:
            config_schema.validate(config)
        except SchemaError as se:
            raise se

        return config["hushbot"]


async def is_staff(user: discord.Member, required_role) -> bool:
    return required_role in user.roles


class Helpers:
    def __init__(self):
        self.config = load_config()

    async def is_command(self, message: discord.Message, required_role) -> bool:
        return message.content.startswith(self.config["general"]["prefix"]) \
               and not message.author.bot \
               and await is_staff(message.author, required_role)

    async def get_command(self, message: discord.Message):
        ctx = message.content[len(self.config["general"]["prefix"]):].split(" ")
        return ctx[0], ctx[1:]

    async def has_args(self, args, expected, message):
        if len(args) >= expected:
            return True

        await message.channel.send("Missing args")
        return False
