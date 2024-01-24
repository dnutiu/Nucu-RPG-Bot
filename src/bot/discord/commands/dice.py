from disnake.ext import commands

from src.dice.dice import DiceRoller


class DiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll", aliases=["r"])
    async def roll(self, ctx, dice_expression: str):
        """
        A die can be rolled using the following expression:
        - 1d20 will roll a 20-faceted die and output the result a random number between 1 and 20.
        - 1d100 will roll a 100 faceted die.
        - 2d20 will roll a two d20 dies and multiply the result by two.
        - 2d20+5 will roll a two d20 dies and multiply the result by two and ads 5.
        """
        if dice_expression == "":
            return
        if dice_expression == "0/0":  # easter eggs
            return await ctx.send("What do you expect me to do, destroy the universe?")

        try:
            roll_result = DiceRoller.roll_simple(dice_expression)
            await ctx.send(f"You rolled: {roll_result}")
        except ValueError as e:
            await ctx.send(f"Roll failed: {e}")
