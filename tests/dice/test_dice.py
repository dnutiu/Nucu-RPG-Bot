import pytest

from src.dice.dice import DiceRoller


@pytest.fixture()
def dice_roller():
    return DiceRoller()


@pytest.mark.parametrize(
    "expression, range_min, range_max",
    [
        # normal roll
        ("d20", 1, 20),
        ("d12", 1, 12),
        ("d10", 1, 10),
        ("d8", 1, 8),
        ("d6", 1, 6),
        ("d4", 1, 4),
        # multiple dies
        ("2d20", 2, 40),
        ("2d12", 2, 24),
        ("2d10", 2, 20),
        ("2d8", 2, 16),
        ("2d6", 2, 12),
        ("2d4", 2, 8),
        # positive modifier
        ("d20+1", 1, 21),
        ("d12+1", 1, 13),
        ("d10+1", 1, 11),
        ("d8+1", 1, 9),
        ("d6+1", 1, 7),
        ("d4+1", 1, 5),
        # negative modifier
        ("d20-1", 1, 19),
        ("d12-1", 1, 11),
        ("d10-1", 1, 9),
        ("d8-1", 1, 7),
        ("d6-1", 1, 5),
        ("d4-1", 1, 3),
        # white-space in expression
        ("1d20 +0", 1, 20),
        ("1d12 + 0", 1, 12),
        ("1 d10 + 0", 1, 10),
        ("1 d8 +0", 1, 8),
        ("1 d 6 +0", 1, 6),
        ("1d 4 +0", 1, 4),
    ],
)
def test_die_roller_die_roll_simple(expression, range_min, range_max, dice_roller):
    # let the dies roll...
    for i in range(100):
        result = dice_roller.roll_simple(expression)
        assert range_min <= result <= range_max


@pytest.mark.parametrize(
    "expression, range_min, range_max",
    [
        # normal roll
        ("zd20", 0, 20),
        ("zd12", 0, 12),
        ("zd10", 0, 10),
        ("zd8", 0, 8),
        ("zd6", 0, 6),
        ("zd4", 0, 4),
        # multiple dies
        ("2zd20", 0, 40),
        ("2zd12", 0, 24),
        ("2zd10", 0, 20),
        ("2zd8", 0, 16),
        ("2zd6", 0, 12),
        ("2zd4", 0, 8),
        # positive modifier
        ("zd20+1", 0, 21),
        ("zd12+1", 0, 13),
        ("zd10+1", 0, 11),
        ("zd8+1", 0, 9),
        ("zd6+1", 0, 7),
        ("zd4+1", 0, 5),
        # negative modifier
        ("zd20-1", 0, 19),
        ("zd12-1", 0, 11),
        ("zd10-1", 0, 9),
        ("zd8-1", 0, 7),
        ("zd6-1", 0, 5),
        ("zd4-1", 0, 3),
        # white-space in expression
        ("1zd20 +0", 0, 20),
        ("1zd12 + 0", 0, 12),
        ("1 zd10 + 0", 0, 10),
        ("1 zd8 +0", 0, 8),
        ("1 zd 6 +0", 0, 6),
        ("1zd 4 +0", 0, 4),
    ],
)
def test_die_roller_zero_die_roll_simple(expression, range_min, range_max, dice_roller):
    # let the dies roll...
    for i in range(100):
        result = dice_roller.roll_simple(expression)
        assert range_min <= result <= range_max


@pytest.mark.parametrize(
    "expression",
    [
        "20d",
        "d",
        "zd",
        "20",
        "20+3",
        "20q+3",
        "123q*3",
        "20d*3",
        "20d20*3",
        "20d20/3",
    ],
)
def test_die_roller_die_parsing_fail(expression, dice_roller):
    with pytest.raises(ValueError):
        dice_roller.roll_simple(expression)


def test_die_roller_roll(dice_roller):
    for i in range(100):
        result = dice_roller.roll("d20 + d20 adv d20+5 dis d12+3")
        assert 1 <= result.total <= 15
        assert len(result.dies) == 4
