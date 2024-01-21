import pytest

from src.dice.dice import DiceRoller


@pytest.fixture()
def dice_roller():
    return DiceRoller()


@pytest.mark.parametrize(
    "expression, range_min, range_max",
    [
        ("d20", 1, 20),
        ("d12", 1, 12),
        ("d10", 1, 10),
        ("d8", 1, 8),
        ("d6", 1, 6),
        ("d4", 1, 4),
        ("2d20", 2, 40),
        ("2d12", 2, 24),
        ("2d10", 2, 20),
        ("2d8", 2, 16),
        ("2d6", 2, 12),
        ("2d4", 2, 8),
        ("d20+1", 1, 21),
        ("d12+1", 1, 13),
        ("d10+1", 1, 11),
        ("d8+1", 1, 9),
        ("d6+1", 1, 7),
        ("d4+1", 1, 5),
        ("d20-1", 1, 19),
        ("d12-1", 1, 11),
        ("d10-1", 1, 9),
        ("d8-1", 1, 7),
        ("d6-1", 1, 5),
        ("d4-1", 1, 3),
    ],
)
def test_die_roll(expression, range_min, range_max, dice_roller):
    # let the dies roll...
    for i in range(100):
        result = dice_roller.roll(expression)
        assert range_min <= result <= range_max
