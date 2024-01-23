import logging

import disnake
from disnake.ext.commands import bot

from src.bot.discord.commands.dice import DiceCog


class NucuBot(bot.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._logger = logging.getLogger(__name__)

    @staticmethod
    def create(command_prefix: str = ".") -> "NucuBot":
        intents = disnake.Intents.all()
        discord_bot = NucuBot(intents=intents, command_prefix=command_prefix)
        discord_bot.add_cog(DiceCog(discord_bot))
        return discord_bot

    async def on_ready(self):
        self._logger.info(f"Logged on as {self.user}!")
