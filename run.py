from os import getenv

from src.bot import Hush

client = Hush()
client.run(getenv("BOT_TOKEN"))
