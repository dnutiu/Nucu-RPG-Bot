from src.bot.discord.commands.dice import DiceCog
from src.dice.dice import DieExpressionResult, DieRollResult


def test_format_die_result_to_message():
    message = DiceCog.format_die_result_to_fields(
        DieExpressionResult(
            total=25,
            dies=[
                DieRollResult(
                    result=10, modifier=5, rolls=[10], type="d", die_number=20
                ),
                DieRollResult(
                    result=15, modifier=0, rolls=[10, 5], type="d", die_number=20
                ),
            ],
        ),
    )
    assert message == [
        ("- #1 🎲 d20", "Res: 10, Mod: 5, Rolls: [10]"),
        ("- #2 🎲 d20", "Res: 15, Mod: 0, Rolls: [10, 5]"),
    ]
