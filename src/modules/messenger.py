from discord import Colour, Embed, TextChannel


class Messenger:
    """Handles messages sent to discord."""

    def __init__(self, log_channel: TextChannel, alert_channel: TextChannel) -> None:
        self.log_channel = log_channel
        self.alert_channel = alert_channel

    async def notify(
        self,
        notify_type: str,
        user: int,
        word: str,
        original: str,
        action: str = "",
    ) -> None:
        """Send message to discord."""
        channel = None

        if notify_type == "Log":
            channel = self.log_channel
            embed = Embed(title=f"Hush | {notify_type}", colour=Colour.orange())

            embed.add_field(name="Action", value=f"```{action}```", inline=False)
        elif notify_type == "Alert":
            channel = self.alert_channel
            embed = Embed(title=f"Hush | {notify_type}", colour=Colour.red())

        embed.add_field(name="User", value=f"<@{user}>", inline=False)

        embed.add_field(
            name="Reason",
            value=f"Use of blacklisted word:\n```{word}```",
            inline=False,
        )

        embed.add_field(
            name="Original Message", value=f"```{original}```", inline=False
        )

        await channel.send(embed=embed)  # type: ignore
