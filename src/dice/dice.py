import typing

from src.dice.parser import DieParser


class DiceRoller:
    """
    DiceRoller is a simple class that allows you to roll dices.

    A die can be rolled using the following expression:
    - 1d20 will roll a 20-faceted die and output the result a random number between 1 and 20.
    - 1d100 will roll a 100 faceted die.
    - 2d20 will roll a two d20 dies and multiply the result by two.
    - 2d20+5 will roll a two d20 dies and multiply the result by two and ads 5.
    """

    _parser = DieParser.create()

    @staticmethod
    def roll(expression: str, *, advantage: typing.Optional[bool] = None) -> int:
        """
        Roll die and return the result.
        :param expression: The die expression.
        :param advantage: Optionally, rolls a die with advantage or disadvantage.
        :return: The die result.
        """
        if advantage is None:
            return DiceRoller._parser.parse(expression)
        elif advantage is True:
            return DiceRoller.roll_with_advantage(expression)
        elif advantage is False:
            return DiceRoller.roll_with_disadvantage(expression)

    @staticmethod
    def roll_with_advantage(expression: str) -> int:
        """
        Roll two dies and return the highest result.
        :param expression: The die expression.
        :return: The die result.
        """
        one = DiceRoller._parser.parse(expression)
        two = DiceRoller._parser.parse(expression)
        return max(one, two)

    @staticmethod
    def roll_with_disadvantage(expression: str) -> int:
        """
        Roll two dies and return the lowest result.
        :param expression: The die expression.
        :return: The die result.
        """
        one = DiceRoller._parser.parse(expression)
        two = DiceRoller._parser.parse(expression)
        return min(one, two)
