import dataclasses
import typing

from src.dice.parser import DieParser


@dataclasses.dataclass
class DieRollResult:
    """
    DieRoll is the result of a die roll.
    """

    result: int
    modifier: int
    rolls: typing.List[int]
    die_number: int
    type: str


@dataclasses.dataclass
class DieExpressionResult:
    """
    DiceResult is the result of a dice roll expression.
    """

    total: int
    dies: typing.List[DieRollResult]


class DiceRoller:
    """
    DiceRoller is a simple class that allows you to roll dices.

    A die can be rolled using the following expression:
    - 1d20 will roll a 20-faceted die and output the result a random number between 1 and 20.
    - 1d100 will roll a 100 faceted die.
    - 2d20 will roll two d20 dies and multiply the result by two.
    - 2d20+5 will roll two d20 dies add them together then add 5 to the result.
    """

    _parser = DieParser.create()

    @staticmethod
    def roll_simple(expression: str) -> int:
        """
        Roll die and return the result.
        :param expression: The die expression.
        :return: The die result.
        """
        result = DiceRoller._parser.parse(expression)
        return result.get("total")

    @staticmethod
    def roll(expression: str) -> DieExpressionResult:
        """
        Roll die and return the DiceResult.
        :param expression: The die expression.
        :return: The die result.
        """
        result = DiceRoller._parser.parse(expression)

        dies = []
        for die in result.get("dies", []):
            dies.append(
                DieRollResult(
                    modifier=die.get("modifier", 0),
                    result=die.get("result"),
                    rolls=die.get("rolls"),
                    type=die.get("type"),
                    die_number=die.get("die_number"),
                )
            )
        return DieExpressionResult(total=result.get("total"), dies=dies)
