import random
from tatsu.ast import AST


# noinspection PyMethodMayBeStatic
class DieSemantics:
    def number(self, ast):
        return int(ast)

    def start(self, ast):
        return ast.get("die").get("result")

    def die(self, ast):
        if not isinstance(ast, AST):
            return ast
        # the number of dies is optional; by default, we have one die
        number_of_dies = ast.get("number_of_dies") or 1

        die_type = ast.get("die_type")
        die_number = ast.get("die_number")

        # modifier is optional, if it doesn't exist we use 0
        die_modifier = ast.get("modifier") or 0

        minimum_value_for_die = 1
        if die_type == "zd":
            # zero-based die can output 0.
            minimum_value_for_die = 0

        rolls = [
            random.randint(minimum_value_for_die, die_number)
            for _ in range(number_of_dies)
        ]

        return {
            "result": max(sum(rolls) + die_modifier, minimum_value_for_die),
            "die_type": die_type,
            "roll_history": rolls,
            "modifier": die_modifier,
        }

    def die_modifier(self, ast):
        if not isinstance(ast, AST):
            return ast
        op = ast.get("op")
        modifier = ast.get("modifier", 0)
        if op == "+":
            return modifier
        else:
            return -modifier
