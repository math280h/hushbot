from discord import Embed, Colour


class Messenger:
    def __init__(self, log_channel, alert_channel):
        self.log_channel = log_channel
        self.alert_channel = alert_channel

    async def notify(self, notify_type, user, word, original, action=None):
        channel = None

        if notify_type == "Log":
            channel = self.log_channel
            embed = Embed(title=f"Hush | {notify_type}", colour=Colour.orange())

            embed.add_field(
                name=f"Action",
                value=f"```{action}```",
                inline=False
            )
        elif notify_type == "Alert":
            channel = self.alert_channel
            embed = Embed(title=f"Hush | {notify_type}", colour=Colour.red())

        embed.add_field(
            name=f"User",
            value=f"<@{user}>",
            inline=False
        )

        embed.add_field(
            name=f"Reason",
            value=f"Use of blacklisted word:\n```{word}```",
            inline=False
        )

        embed.add_field(
            name=f"Original Message",
            value=f"```{original}```",
            inline=False
        )

        await channel.send(embed=embed)
