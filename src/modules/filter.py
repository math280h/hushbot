from redis import Redis


class Filter:
    """Class for text filtering."""

    def __init__(self, r: Redis) -> None:
        self.r = r

    async def filter(self, text: str) -> tuple:
        """Filter message content."""
        content = "".join(e for e in text if e.isalnum())

        words = self.r.keys()

        for word in words:
            if word.decode() in content:
                action = self.r.get(word.decode()).decode()
                if action == "alert":
                    return "alert", word.decode()
                elif action == "ban":
                    return "ban", word.decode()
                elif action == "delete":
                    return "del", word.decode()

        return None, None
