import random
from tatsu.ast import AST


# noinspection PyMethodMayBeStatic
class DieSemantics:
    def number(self, ast):
        return int(ast)

    def start(self, ast):
        return ast.get("die")

    def die(self, ast):
        if not isinstance(ast, AST):
            return ast
        number_of_dies = ast.get("number_of_dies") or 1
        die_type = ast.get("die_type")
        die_number = ast.get("die_number") or 1
        die_modifier = ast.get("modifier") or 0
        if die_number <= 0:
            return 0
        # normal die
        if die_type == "d":
            die_sum = sum(
                [random.randint(1, die_number) for _ in range(number_of_dies)]
            )
            # do not let die to underflow
            return max(die_sum + die_modifier, 1)
        # zero-based die can output 0.
        if die_type == "zd":
            die_sum = sum(
                [random.randint(0, die_number) for _ in range(number_of_dies)]
            )
            return max(die_sum + die_modifier, 0)
        raise ValueError(f"Invalid die type: {die_type}")

    def die_modifier(self, ast):
        if not isinstance(ast, AST):
            return ast
        op = ast.get("op")
        modifier = ast.get("modifier", 0)
        if op == "+":
            return modifier
        else:
            return -modifier
