import logging

from src.bot.discord.bot import NucuBot


def main():
    bot = NucuBot.create()
    bot.run("<token here>")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
