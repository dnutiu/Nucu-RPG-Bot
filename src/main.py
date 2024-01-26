import logging

from src.bot.config.configurator import Settings
from src.bot.discord.bot import NucuBot


def main():
    settings = Settings()
    bot = NucuBot.create(
        command_prefix=settings.discord.command_prefix,
        game_name=settings.discord.game_name,
    )
    bot.run(settings.discord.token)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
