import typing
from datetime import datetime

import disnake
from disnake.ext import commands

from src.dice.dice import DiceRoller, DieExpressionResult


class DiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def format_die_result_to_fields(
        die_result: DieExpressionResult,
    ) -> list[typing.Tuple[str, str]]:
        roll_fields = []
        for index, die in enumerate(die_result.dies):
            roll_fields.append(
                (
                    f"- #{index+1} 🎲 {die.type}{die.die_number}",
                    f"Res: {die.result}, Mod: {die.modifier}, Rolls: {die.rolls}",
                )
            )
        return roll_fields

    @commands.command(name="roll", aliases=["r"])
    async def roll(self, ctx, _dice_expression: str):
        """
        A die can be rolled using the following expression:
        - 1d20 will roll a 20-faceted die and output the result a random number between 1 and 20.
        - 1d100 will roll a 100 faceted die.
        - 2d20 will roll a two d20 dies and multiply the result by two.
        - 2d20+5 will roll a two d20 dies and multiply the result by two and ads 5.
        """
        try:
            message: str = ctx.message.clean_content
            dice_expression = message.split(" ", 1)[1]
            if dice_expression == "":
                return
            if dice_expression == "0/0":  # easter eggs
                return await ctx.send(
                    "What do you expect me to do, destroy the universe?"
                )

            die_result: DieExpressionResult = DiceRoller.roll(dice_expression)

            embed = disnake.Embed(
                title=f"{die_result.total} !!",
                description=f"{dice_expression} = {die_result.total}",
                timestamp=datetime.now(),
            )
            embed_fields = self.format_die_result_to_fields(die_result)
            for title, value in embed_fields:
                embed.add_field(title, value, inline=False)

            await ctx.send(
                f"The mighty **{ctx.author.name}** has rolled the dice for a total of **{die_result.total}**!",
                embed=embed,
            )
        except ValueError as e:
            await ctx.send(f"Roll failed: {e}")
